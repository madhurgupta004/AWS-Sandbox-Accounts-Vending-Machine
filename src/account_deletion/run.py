import time
import logging

from botocore.exceptions import ClientError

from account_deletion.helpers import account_id, ACCESS_KEY, SECRET_ACCESS_KEY
from common.boto3_helper import get_boto3_client


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def send_close_account_request():
    response = organization_client.close_account(
        AccountId=account_id
    )
    logging.info(f'Close account request sent for account ID: {account_id}')
    logging.debug(response)


def wait_till_account_closed():
    while True:
        time.sleep(5)
        response = organization_client.describe_account(
            AccountId=account_id
        )
        logging.debug(response)
        if response['Account']['Status'] == 'SUSPENDED':
            logging.info(f'Account {account_id} is now suspended.')
            return
        elif response['Account']['Status'] == 'ACTIVE':
            raise Exception(f'Account suspension failed: {response["CreateAccountStatus"]["FailureReason"]}')
        else:
            logging.info(f'Account suspension in progress...')


if __name__ == "__main__":
    try: 
        organization_client = get_boto3_client('organizations', ACCESS_KEY, SECRET_ACCESS_KEY)
        send_close_account_request()
        wait_till_account_closed()

    except ClientError as ex:
        logging.error(f'ClientError: {ex}')
        raise
    except Exception as ex:
        logging.error(f'Some error occured: {ex}')
        raise