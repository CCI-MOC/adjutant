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

from adjutant.actions.v1 import (projects, users)
from adjutant.common import user_store
from adjutant.actions.utils import validate_steps


class MocNewProjectWithUserAction(projects.NewProjectWithUserAction):
    required = [
        'domain_id',
        'parent_id',
        'project_name',
        'username',
        'email',

        # TODO(knikolla): It should be possible to fetch these from
        # SSO once we support OAuth 2.0 access tokens.
        'organization',
        'organization_role',
        'phone',
        'moc_contact'
    ]

    def __init__(self, *args, **kwargs):
        super(MocNewProjectWithUserAction, self).__init__(*args, **kwargs)


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
        self.set_token_fields(["token"])

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

        if not self.valid:
            return

        id_manager = user_store.IdentityManager()
        user = id_manager.validate_token(token_data['token'])['user']

        # Note(knikolla): Invalid token, exit.
        if not user:
            self.add_note('Received request with invalid token')
            return False

        roles = id_manager.get_roles(user, self.project_id)
        role_names = {role.name for role in roles}
        missing = set(self.roles) - role_names
        if not missing:
            self.action.need_token = False
            self.action.state = "complete"
            self.add_note(
                'Accepted by %s. User already has roles.' % user.name
            )
        else:
            self.roles = list(missing)
            self.grant_roles(user, self.roles, self.project_id)
            self.grant_roles(user, self.inherited_roles, self.project_id, True)

            self.add_note(
                'Accepted by %s. User added with roles %s on project %s.'
                % (user.name, self.roles, self.project_id))
        return True
