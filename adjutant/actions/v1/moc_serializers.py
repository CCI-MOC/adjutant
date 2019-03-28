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

from rest_framework import serializers
from adjutant.actions.v1 import serializers as adjutant_serializers


class MocProjectWithUserSerializer(
    adjutant_serializers.NewProjectWithUserSerializer
):
    organization = serializers.CharField(max_length=64)
    organization_role = serializers.CharField(max_length=64)
    phone = serializers.CharField(max_length=64)
    moc_contact = serializers.CharField(max_length=64)
