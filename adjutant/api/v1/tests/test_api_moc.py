# Copyright (c) 2019 Kristi Nikolla
#
# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock

from rest_framework import status

from adjutant.common.tests import fake_clients
from adjutant.common.tests.utils import AdjutantAPITestCase


@mock.patch('adjutant.common.user_store.IdentityManager',
            fake_clients.FakeManager)
class MocApiTests(AdjutantAPITestCase):

    def test_signup_noauth(self):
        url = "/v1/openstack/sign-up"
        data = {
            'project_name': 'project_name'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_signup_bad_data(self):
        user = fake_clients.FakeUser(
            name="test@example.com", password="123", email="test@example.com")
        fake_clients.setup_identity_cache(users=[user])
        url = "/v1/openstack/sign-up"
        headers = {
            'username': user.name,
            'user_id': user.id,
            'authenticated': True
        }
        data = {
            'project_name': 'demoproject1',
        }
        response = self.client.post(url, data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup(self):
        user = fake_clients.FakeUser(
            name="test@example.com", password="123", email="test@example.com")
        fake_clients.setup_identity_cache(users=[user])
        url = "/v1/openstack/sign-up"
        headers = {
            'username': user.name,
            'user_id': user.id,
            'authenticated': True
        }
        data = {
            'project_name': 'demoproject1',
            'organization': 'Test Org',
            'moc_contact': 'Test Contact',
            'phone': '555 555 5555',
            'organization_role': 'dungeon master'
        }
        response = self.client.post(url, data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
