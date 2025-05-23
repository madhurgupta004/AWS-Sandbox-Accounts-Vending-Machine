import os

from .utils import generate_password
from .boto3_helper import get_boto3_client
from ._arguments import initial_account_data_s3_key


ROOT_OU_ID = 'r-i68s'
SANDBOX_OU_ID = 'ou-i68s-ggbxakm3'
GROUP_NAME = 'Interns'
FINAL_DATA_BUCKET_NAME = 'sandbox-accounts-vending-machine-final-data'
INITIAL_DATA_BUCKET_NAME = 'sandbox-accounts-vending-machine-initial-data'
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

__all__ = [
    'get_boto3_client',
    'generate_password',
    'initial_account_data_s3_key',  
    'GROUP_NAME',
    'ROOT_OU_ID',
    'SANDBOX_OU_ID',
    'ACCESS_KEY',
    'SECRET_ACCESS_KEY',
    'FINAL_DATA_BUCKET_NAME',
    'INITIAL_DATA_BUCKET_NAME'
]