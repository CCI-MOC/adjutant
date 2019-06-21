# Copyright (C) 2015 Catalyst IT Ltd
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Django settings for Adjutant.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import yaml
from adjutant.utils import setup_task_settings
from adjutant.exceptions import ConfigurationException
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'adjutant.actions',
    'adjutant.api',
    'adjutant.notifications',
    'adjutant.tasks',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'adjutant.middleware.KeystoneHeaderUnwrapper',
    'adjutant.middleware.RequestLoggingMiddleware'
)

if 'test' in sys.argv:
    # modify MIDDLEWARE_CLASSES
    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
    MIDDLEWARE_CLASSES.remove('adjutant.middleware.KeystoneHeaderUnwrapper')
    MIDDLEWARE_CLASSES.append('adjutant.middleware.TestingHeaderUnwrapper')

ROOT_URLCONF = 'adjutant.urls'

WSGI_APPLICATION = 'adjutant.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'NAME': 'default',
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': ['/etc/adjutant/templates/'],
        'NAME': 'include_etc_templates',
    },
]

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'adjutant.api.exception_handler.exception_handler',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PERMISSION_CLASSES': [],
}

# Setup of local settings data
if 'test' in sys.argv:
    from adjutant import test_settings
    CONFIG = test_settings.conf_dict
else:
    config_file = "/etc/adjutant/conf.yaml"
    if not os.path.isfile(config_file):
        print("%s does not exist. Reverting to default config file." %
              config_file)
        config_file = "conf/conf.yaml"
    with open(config_file) as f:
        CONFIG = yaml.load(f, Loader=yaml.FullLoader)

SECRET_KEY = CONFIG['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.get('DEBUG', False)

if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
        'rest_framework.renderers.BrowsableAPIRenderer')

ALLOWED_HOSTS = CONFIG.get('ALLOWED_HOSTS', [])

for app in CONFIG['ADDITIONAL_APPS']:
    INSTALLED_APPS = list(INSTALLED_APPS)
    INSTALLED_APPS.append(app)

# NOTE(adriant): Because the order matters, we want this import to be last
# so the startup checks run after everything is imported.
INSTALLED_APPS.append("adjutant.startup")

DATABASES = CONFIG['DATABASES']

LOGGING = CONFIG['LOGGING']


EMAIL_BACKEND = CONFIG['EMAIL_SETTINGS']['EMAIL_BACKEND']
EMAIL_TIMEOUT = 60

EMAIL_HOST = CONFIG['EMAIL_SETTINGS'].get('EMAIL_HOST')
EMAIL_PORT = CONFIG['EMAIL_SETTINGS'].get('EMAIL_PORT')
EMAIL_HOST_USER = CONFIG['EMAIL_SETTINGS'].get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = CONFIG['EMAIL_SETTINGS'].get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = CONFIG['EMAIL_SETTINGS'].get('EMAIL_USE_TLS', False)
EMAIL_USE_SSL = CONFIG['EMAIL_SETTINGS'].get('EMAIL_USE_SSL', False)

# setting to control if user name and email are allowed
# to have different values.
USERNAME_IS_EMAIL = CONFIG['USERNAME_IS_EMAIL']

# Keystone admin credentials:
KEYSTONE = CONFIG['KEYSTONE']

TOKEN_SUBMISSION_URL = CONFIG.get('TOKEN_SUBMISSION_URL')
if TOKEN_SUBMISSION_URL:
    print("'TOKEN_SUBMISSION_URL' is deprecated, use 'HORIZON_URL' instead")

HORIZON_URL = CONFIG.get('HORIZON_URL')

if not HORIZON_URL and not TOKEN_SUBMISSION_URL:
    raise ConfigurationException("Must supply 'HORIZON_URL'")

TOKEN_EXPIRE_TIME = CONFIG['TOKEN_EXPIRE_TIME']

DEFAULT_ACTION_SETTINGS = CONFIG['DEFAULT_ACTION_SETTINGS']

TASK_SETTINGS = setup_task_settings(
    CONFIG['DEFAULT_TASK_SETTINGS'],
    CONFIG['DEFAULT_ACTION_SETTINGS'],
    CONFIG['TASK_SETTINGS'])

DEFAULT_TASK_SETTINGS = CONFIG['DEFAULT_TASK_SETTINGS']

PLUGIN_SETTINGS = CONFIG.get('PLUGIN_SETTINGS', {})

ROLES_MAPPING = CONFIG['ROLES_MAPPING']

TOKEN_CACHE_TIME = CONFIG.get('TOKEN_CACHE_TIME', 60)

PROJECT_QUOTA_SIZES = CONFIG.get('PROJECT_QUOTA_SIZES')

QUOTA_SIZES_ASC = CONFIG.get('QUOTA_SIZES_ASC', [])

ACTIVE_DELEGATE_APIS = CONFIG.get(
    'ACTIVE_DELEGATE_APIS',
    [
        'UserRoles',
        'UserDetail',
        'UserResetPassword',
        'UserList',
        'RoleList'
    ])

# Default services for which to check and update quotas for
QUOTA_SERVICES = CONFIG.get(
    'QUOTA_SERVICES',
    {'*': ['cinder', 'neutron', 'nova']})


# Dict of DelegateAPIs and their url_paths.
# - This is populated by registering DelegateAPIs.
DELEGATE_API_CLASSES = {}

# Dict of actions and their serializers.
# - This is populated from the various model modules at startup:
ACTION_CLASSES = {}

TASK_CLASSES = {}

NOTIFICATION_ENGINES = {}
