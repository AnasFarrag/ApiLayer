import os
from pathlib import Path
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
DATA_UPLOAD_MAX_MEMORY_SIZE = 10458760 #(10458760/(1024*1024)) = 10MB

# CLOUD cradintials
CLOUD_URL = 'https://cloud.variiance.com/'
CLOUD_USERNAME = 'muhammed'
CLOUD_PASSWORD = 'muhammed123Muhammed'

# ERP cradentials
ERP_URL = 'https://erpdev.variiance.com/'
ERP_TOKEN = 'token c14f1f8e6c0b04f:3354d1ba0f8c414'

# SSO cradentials
SSO_URL = 'https://sso.variiance.com/auth/admin/realms/Variiance/users/{}/reset-password'

# Fawry End Point
FAWRY_ERP_END_POINT = 'payment_portal/en/fawry_callback'


# Working Environment
ENV = 'development'
