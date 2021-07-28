import os
from pathlib import Path
import owncloud
from datetime import datetime
# Application definition
INSTALLED_APPS = [
    'callapi',
    'dashboard',
    'fawry',
    'user',
    'telegram',
]

# Define the base dir of the project
BASE_DIR = str(Path(__file__).resolve().parent) + '/'
# the following line do the same thing
# BASE_DIR = os.path.abspath(os.path.join('../', os.path.dirname(__file__ ))) + '\\'

# Maxmum size of the uploaded files
# DATA_UPLOAD_MAX_MEMORY_SIZE = 10458760 #(10458760/(1024*1024)) = 10MB

# Allawed Extensions that can be uploaded on server
ALLOWED_EXTENSIONS = ['gif', 'jpeg','jpg', 'bmp', 'png']

# CLOUD cradintials
CLOUD_URL = 'https://cloud.variiance.com/'
CLOUD_USERNAME = 'muhammed'
CLOUD_PASSWORD = 'muhammed123Muhammed'

# Cloud login

# set CLOUD URL
CLOUD = owncloud.Client(CLOUD_URL)
# Login to CLOUD
CLOUD.login(CLOUD_USERNAME, CLOUD_PASSWORD)
# Base directory of all users in cloud
USERS_BASE_DIR_IN_CLOUD = 'upload/'

DATE = datetime.now()
YEAR = DATE.year
MONTH = DATE.month
UPLOAD_DIR_IN_CLOUD = f'{USERS_BASE_DIR_IN_CLOUD}{YEAR}/{MONTH}'


# ERP cradentials
ERP_URL = 'https://erpdev.variiance.com/'
ERP_TOKEN = 'token c14f1f8e6c0b04f:3354d1ba0f8c414'

# SSO cradentials
SSO_BASE_URL = 'https://sso.variiance.com/'
SSO_RESET_PASSWORD_URL = SSO_BASE_URL + 'auth/admin/realms/Variiance/users/{}/reset-password'
SSO_UPDATE_USER_URL = SSO_BASE_URL + 'auth/admin/realms/Variiance/users/{}'
SSO_TOKEN = 'Bearer {}'
SSO_LOGIN = SSO_BASE_URL + 'auth/realms/Variiance/protocol/openid-connect/token'
SSO_INSTRUCTOR_ROLE = SSO_BASE_URL + 'auth/admin/realms/Variiance/users/{}/' + 'role-mappings/clients/facef935-9db4-494a-a8f7-f9d3680e2f28'


# Fawry End Point
FAWRY_ERP_END_POINT = 'payment_portal/en/fawry_callback'

# check phone endpoint
ERP_CHECK_PHONE_URL = 'profile/ar/check_phone'

# Working Environment
ENV = 'production'

# Uploaded Media folder
UPLOAD_DIR = BASE_DIR + 'media/'

USER_LANGUAGE =  SSO_BASE_URL + 'auth/admin/realms/Variiance/users/{}'

#static Dir
STATIC_DIR = BASE_DIR + 'static/'

#Certifation
ERP_CERTIFICATE =  ERP_URL + 'api/resource/Enrollment/{}'

# set CLOUD URL
CLOUD = owncloud.Client(CLOUD_URL)
# Login to CLOUD
CLOUD.login(CLOUD_USERNAME, CLOUD_PASSWORD)
# Base directory of all users in cloud
USERS_BASE_DIR_IN_CLOUD = 'upload/'

DATE = datetime.now()
YEAR = DATE.year
MONTH = DATE.month
UPLOAD_DIR_IN_CLOUD = f'{USERS_BASE_DIR_IN_CLOUD}{YEAR}/{MONTH}'
STATIC_DIR = BASE_DIR + 'static/'


# Services Domains
SSO_DOMAIN = 'sso.variiance.com'
CLOUD_DOMAIN = 'cloud.variiance.com'
ERP_DOMAIN = 'erpdev.variiance.com'
