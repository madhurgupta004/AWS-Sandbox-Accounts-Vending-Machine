from helpers import get_boto3_client, access_key, secret_access_key

from run import get_initial_account_data

client = get_boto3_client('s3' , access_key=access_key, secret_access_key=secret_access_key)
print(get_initial_account_data(client))