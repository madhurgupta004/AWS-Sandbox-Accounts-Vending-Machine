import json
import time
import logging

from typing import List
from botocore.exceptions import ClientError

from helpers.boto3_helper import get_boto3_client
from helpers.helper import generate_password
from helpers._arguments import access_key, secret_access_key

ROOT_OU_ID = 'r-i68s'
SANDBOX_OU_ID = 'ou-i68s-ggbxakm3'
GROUP_NAME = 'Interns'

organization_client = get_boto3_client('organizations', access_key, secret_access_key)
account_data = json.load(open('test_events/create_account.json'))

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def create_account():
    logging.info('Initialing account creation...')
    response = organization_client.create_account(
        Email=account_data['accountEmail'],
        AccountName=account_data['accountName'],
        RoleName=account_data['roleName'],
        IamUserAccessToBilling='ALLOW',
    ) 
    logging.debug(response)
    account_data['accountRequestId'] = response['CreateAccountStatus']['Id']
    logging.info(f"Account creation initiated with request ID: {account_data['accountRequestId']}")


def wait_until_account_created():
    while True:
        time.sleep(5)
        response = organization_client.describe_create_account_status(
            CreateAccountRequestId=account_data['accountRequestId']
        )
        logging.debug(response)
        if response['CreateAccountStatus']['State'] == 'SUCCEEDED':
            account_data['accountId'] = response['CreateAccountStatus']['AccountId']
            logging.info(f"Account created successfully with ID: {account_data['accountId']}")
            return
        elif response['CreateAccountStatus']['State'] == 'FAILED':
            raise Exception(f'Account creation failed: {response["CreateAccountStatus"]["FailureReason"]}')
        else:
            logging.info(f'Account Creation in progress...')
    

def move_into_ou():
    response = organization_client.move_account(
        AccountId=account_data['accountId'],
        SourceParentId=ROOT_OU_ID,
        DestinationParentId=SANDBOX_OU_ID,
    )
    logging.debug(response)
    logging.info(f"Account moved into Sandbox OU")


def get_iam_client_of_member_account():
    sts_client = get_boto3_client('sts', access_key, secret_access_key)
    role_arn = f"arn:aws:iam::{account_data['accountId']}:role/{account_data['roleName']}"

    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName='Create-Users-in-member-account'
    )
    logging.debug(response)
    credentials = response['Credentials']

    iam_client = get_boto3_client(
        'iam',
        access_key=credentials['AccessKeyId'],
        secret_access_key=credentials['SecretAccessKey'],
        session_token=credentials['SessionToken']
    )
    return iam_client


def create_user_for_manager(iam_client):
    manager_user_name = account_data['managerUserName']
    initial_password = generate_password()

    response = iam_client.create_user(UserName=manager_user_name)
    logging.debug(response)

    response = iam_client.create_login_profile(
        UserName=manager_user_name,
        Password=initial_password,
        PasswordResetRequired=True
    )
    logging.debug(response)

    response = iam_client.attach_user_policy(
        UserName=manager_user_name,
        PolicyArn='arn:aws:iam::aws:policy/AdministratorAccess'
    )
    logging.debug(response)

    send_welcome_email(account_data['managerEmail'], manager_user_name, initial_password)
    logging.info(f'User for manager {account_data['managerUserName']} is created and email sent. Password is {initial_password}')


def create_group_for_interns(iam_client):
    response = iam_client.create_group(
        GroupName=GROUP_NAME
    )
    logging.debug(response)
    logging.info(f'Group {GROUP_NAME} created successfully.')


def attach_policies_to_interns_group(iam_client):
    for policy_arn in account_data['internsGroupPolicyARNs']:
        response = iam_client.attach_group_policy(
            GroupName=GROUP_NAME,
            PolicyArn=policy_arn
        )
        logging.debug(response)
        logging.info(f'Policy {policy_arn} attached to group {GROUP_NAME}.')


def create_users_for_interns(iam_client):
    for user in account_data['users']:
        user_name = user['userName']
        user_email = user['email']
        initial_password = generate_password()

        response = iam_client.create_user(UserName=user_name)
        logging.debug(response)

        response = iam_client.create_login_profile(
            UserName=user_name,
            Password=initial_password,
            PasswordResetRequired=True
        )
        logging.debug(response)

        response = iam_client.add_user_to_group(
            GroupName=GROUP_NAME,
            UserName=user_name
        )
        logging.debug(response)

        send_welcome_email(user_email, user_name, initial_password)
        logging.info(f'User {user_name} created, added to group {GROUP_NAME}. Password is {initial_password}')


def get_scp_ids() -> List[str]:
    all_scps = []
    next_token = None
    while True:
        if next_token:
            response = organization_client.list_policies(
                Filter='SERVICE_CONTROL_POLICY',
                NextToken=next_token
            )
        else:
            response = organization_client.list_policies(
                Filter='SERVICE_CONTROL_POLICY',
            )
        logging.debug(response)
        all_scps.extend(response['Policies'])
        next_token = response.get('NextToken')
        if not next_token:
            break

    scp_ids = [scp['Id'] for scp in all_scps if scp['Name'] in account_data['serviceControlPolicies']]
    return scp_ids


def attach_scps_to_account(scp_ids):
    print(scp_ids)
    for scp_id in scp_ids:
        response = organization_client.attach_policy(
            PolicyId=scp_id,
            TargetId=account_data['accountId']
        )
        logging.debug(response)
        logging.info(f'SCP {scp_id} attached.')


def send_welcome_email(to_email, username, initial_password, region="us-east-1"):
    ses = get_boto3_client('ses', access_key=access_key, secret_access_key=secret_access_key, region_name=region)

    login_url = f"https://{account_data['accountId']}.signin.aws.amazon.com/console"

    subject = "Your AWS IAM User Account Details"
    body_text = f"""Hello,

            Your AWS IAM user has been created.

            Username: {username}
            Initial Password: {initial_password}
            Console Sign-in Link: {login_url}

            Please sign in and reset your password immediately.

            Thanks,
            AWS Admin Team
            """
    response = ses.send_email(
        Source="madhurgupta590+ses@gmail.com",  
        Destination={'ToAddresses': [to_email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {
                'Text': {'Data': body_text}
            }
        }
    )
    logging.debug(response)
    logging.info(f"Email sent to {username} Message ID: {response['MessageId']}")


def upload_account_details_to_s3():
    key_name = f'created_account_data_{account_data['accountName']}.json'
    file_name = f'test_events/{key_name}'

    with open(file_name, 'w') as f:
        json.dump(account_data, f, indent=4)

    s3_client = get_boto3_client('s3', access_key, secret_access_key)
    bucket_name = 'vending-machine-account-details'
    s3_client.upload_file(file_name, bucket_name, key_name)
    logging.info(f'Account details uploaded to S3 bucket {bucket_name}.')


def main():
    try: 
        logging.info(account_data)
        create_account()
        wait_until_account_created()
        move_into_ou()
        member_account_iam_client = get_iam_client_of_member_account()

        create_user_for_manager(member_account_iam_client)
        create_group_for_interns(member_account_iam_client)
        attach_policies_to_interns_group(member_account_iam_client)
        create_users_for_interns(member_account_iam_client)

        scp_ids = get_scp_ids()
        attach_scps_to_account(scp_ids)
        upload_account_details_to_s3()
        logging.info(f'Final account data: {account_data}')
    except KeyError as ex:
        logging.error(f'Invalid Input JSON File: {ex}')
        raise
    except ClientError as ex:
        logging.error(f'ClientError: {ex}')
        raise
    except Exception as ex:
        logging.error(f'Some error occured: {ex}')
        raise

main()