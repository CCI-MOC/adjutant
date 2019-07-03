import os
import uuid

import openstack as openstacksdk
import pytest

from . import utils


@pytest.fixture()
def openstack() -> openstacksdk.connection.Connection:
    c = openstacksdk.connection.Connection(
        auth=dict(
            auth_url=os.environ.get('OS_AUTH_URL'),
            username=os.environ.get('OS_USERNAME'),
            password=os.environ.get('OS_PASSWORD'),
            project_name=os.environ.get('OS_PROJECT_NAME'),
            project_domain_name='Default',
            user_domain_name='Default'),
        identity_api_version='3',
        identity_interface='public')  # type: openstacksdk.connection.Connection
    yield c

    c.close()


@pytest.fixture(scope='function')
def domain(openstack):
    domain_name = 'adjutant-tests-%s' % uuid.uuid4().hex
    domain = openstack.create_domain(domain_name, enabled=True)

    yield domain

    assert domain.name not in ['Default', 'moc']
    openstack.update_domain(domain, enabled=False)
    openstack.delete_domain(domain)


def test_signup(openstack, domain):
    user_password = uuid.uuid4().hex
    user = openstack.create_user(uuid.uuid4().hex,
                                 domain_id=domain.id,
                                 password=user_password)

    user_session = utils.authenticate_user(user, user_password)
    token = user_session.get_token()

    assert token is not None
