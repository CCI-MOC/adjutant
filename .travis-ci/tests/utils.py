import os

from openstack.identity.v3.user import User
from keystoneauth1.identity import v3
from keystoneauth1 import session


def authenticate_user(user: User, password=None,
                      project_name=None) -> session:
    auth = v3.Password(
      auth_url=os.environ.get('OS_AUTH_URL'),
      username=user.name,
      user_domain_name=user.domain_id,
      password=password,
      project_name=project_name,
      project_domain_name=user.domain_id if project_name else None,
    )
    return session.Session(auth)
