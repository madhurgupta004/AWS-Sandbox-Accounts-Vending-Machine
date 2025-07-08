import os

from .utils import generate_password
from ._arguments import final_account_data_bucket, source_email, root_ou, sandbox_ou, ses_region

GROUP_NAME = 'Interns'
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
ROLE_FOR_MANAGEMENT_ACCOUNT = 'OrganizationAccountAccessRole'

__all__ = [
    'root_ou',
    'sandbox_ou',
    'ses_region',
    'source_email',
    'final_account_data_bucket',
    'generate_password',  
    'GROUP_NAME',
    'ACCESS_KEY',
    'SECRET_ACCESS_KEY',
    'ROLE_FOR_MANAGEMENT_ACCOUNT'
]