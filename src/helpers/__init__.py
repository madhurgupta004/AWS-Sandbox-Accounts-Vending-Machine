import os

from .utils import generate_password
from .boto3_helper import get_boto3_client


ROOT_OU_ID = 'r-i68s'
SANDBOX_OU_ID = 'ou-i68s-ggbxakm3'
GROUP_NAME = 'Interns'
FINAL_DATA_BUCKET_NAME = 'sandbox-accounts-data-bucket'
SOURCE_EMAIL_ADDRESS = 'madhurgupta590+ses@gmail.com'
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

__all__ = [
    'get_boto3_client',
    'generate_password',  
    'GROUP_NAME',
    'ROOT_OU_ID',
    'SANDBOX_OU_ID',
    'ACCESS_KEY',
    'SECRET_ACCESS_KEY',
    'SOURCE_EMAIL_ADDRESS',
    'FINAL_DATA_BUCKET_NAME',
]