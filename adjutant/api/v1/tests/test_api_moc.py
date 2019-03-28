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

import mock

from rest_framework import status
from django.conf import settings

from adjutant.common.tests.fake_clients import (FakeManager,
                                                setup_identity_cache)
from adjutant.common.tests.utils import AdjutantAPITestCase


@mock.patch('adjutant.common.user_store.IdentityManager',
            FakeManager)
class MocApiTests(AdjutantAPITestCase):

    def test_signup_noauth(self):
        settings.ACTIVE_TASKVIEWS = ['SignUp']
        setup_identity_cache()

        url = "/v1/openstack/sign-up"
        data = {'project_name': 'project_name'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
