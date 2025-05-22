from ._arguments import access_key, secret_access_key
from .utils import generate_password
from .boto3_helper import get_boto3_client

ROOT_OU_ID = 'r-i68s'
SANDBOX_OU_ID = 'ou-i68s-ggbxakm3'
GROUP_NAME = 'Interns'
INITIAL_DATA_BUCKET_NAME = 'sandbox-accounts-vending-machine-initial-data'
FINAL_DATA_BUCKET_NAME = 'sandbox-accounts-vending-machine-final-data'