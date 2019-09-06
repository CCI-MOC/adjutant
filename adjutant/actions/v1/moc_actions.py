# Copyright (c) 2019 Kristi Nikolla
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.conf import settings
import paramiko

from adjutant.actions.v1 import (base, misc, projects, users)
from adjutant.common import user_store
from adjutant.actions.utils import validate_steps


class MocNewProjectAction(projects.NewProjectAction):
    required = [
        'domain_id',
        'parent_id',
        'project_name',
        'description',

        # TODO(knikolla): It should be possible to fetch these from
        # SSO once we support OAuth 2.0 access tokens.
        'organization',
        'organization_role',

        'phone',
        'moc_contact'
    ]

    def _get_email(self):
        if settings.USERNAME_IS_EMAIL:
            return self.action.task.keystone_user['username']

    def _validate_domain_id(self):
        # We're fine with projects not matching the domain of the users.
        return True


class MailingListSubscribeAction(base.BaseAction):

    def _get_email(self):
        if settings.USERNAME_IS_EMAIL:
            return self.action.task.keystone_user['username']

    def _mailman(self, command):
        key = paramiko.RSAKey.from_private_key_file(
            self.settings['private_key'])
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.settings['host'],
                       port=self.settings['port'],
                       username=self.settings['user'],
                       pkey=key)

        stdin, stdout, stderr = client.exec_command(command)

        errors = stderr.read()
        if errors:
            self.add_note('Error executing mailman command, check logs.')
            raise ConnectionError(errors)

        # Note(knikolla): Not entirely sure if closing before reading is fine.
        r = stdout.read().decode('utf-8').split('\n')
        client.close()
        return r

    def _is_already_subscribed(self):
        command = ('/usr/lib/mailman/bin/list_members %s'
                   % self.settings['list'])
        members = self._mailman(command)
        return self._get_email() in members

    def _subscribe(self):
        command = (
                'echo %s | /usr/lib/mailman/bin/add_members -r - %s'
                % (self._get_email(), self.settings['list'])
        )
        self._mailman(command)

    def _pre_approve(self):
        self.action.need_token = False
        self.action.valid = True
        self.action.state = 'pending'
        self.action.save()

    def _post_approve(self):
        if self._is_already_subscribed():
            self.add_note('Email %s already subscribed to mailing list.'
                          % self._get_email())
        else:
            self._subscribe()
            self.add_note('Email %s successfully subscribed to mailing list.'
                          % self._get_email())
        self.action.state = 'complete'
        self.action.save()

    def _submit(self, token_data):
        pass


class MocNewUserAction(users.NewUserAction):
    required = [
        'username',
        'email',
        'project_id',
        'roles',
        'inherited_roles',
        'domain_id',
    ]

    def _validate_target_user(self):
        # Note(knikolla): Differently from the default adjutant flow
        # we don't have to deal with creating users. A user will be
        # always be present after they have authenticated since
        # we're using federated identity.

        self.action.state = "pending"
        self.action.need_token = True
        self.set_token_fields(["token", "confirm"])

        return True

    def _validate(self):
        self.action.valid = validate_steps([
            self._validate_role_permissions,
            self._validate_domain_id,
            self._validate_project_id,
            self._validate_target_user,
        ])
        self.action.save()

    def _submit(self, token_data):
        self._validate()

        if not self.valid or not token_data['confirm']:
            return

        id_manager = user_store.IdentityManager()
        user = id_manager.validate_token(token_data['token'])['user']

        # Note(knikolla): Invalid token, exit.
        if not user:
            self.add_note('Received request with invalid token')
            return False

        if self.email != user['name']:
            self.add_note('Email %s not the same as invited user %s'
                          % user['name'], self.email)
            return False

        roles = id_manager.get_roles(user['id'], self.project_id)
        role_names = {role.name for role in roles}
        missing = set(self.roles) - role_names
        if not missing:
            self.action.need_token = False
            self.action.state = "complete"
            self.add_note(
                'Accepted by %s. User already has roles.' % user['name']
            )
        else:
            self.roles = list(missing)
            self.grant_roles(user['id'], self.roles, self.project_id)
            self.grant_roles(user['id'], self.inherited_roles, self.project_id, True)

            self.add_note(
                'Accepted by %s. User added with roles %s on project %s.'
                % (user['name'], self.roles, self.project_id))
        return True
