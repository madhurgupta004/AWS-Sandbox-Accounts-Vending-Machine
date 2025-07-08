import os
import json
import boto3
import logging
import datetime
from botocore.exceptions import ClientError

SANDBOX_OU_ID = os.getenv('SANDBOX_OU_ID')
BUCKET_NAME = os.getenv('ACCOUNTS_DATA_BUCKET')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
ACCOUNTS_MANAGERS_MAPPING_KEY = 'accounts_managers_mapping.json'


today = datetime.date.today()
month_start = today.replace(day=1)
next_month = (month_start + datetime.timedelta(days=32)).replace(day=1)
month_end = next_month - datetime.timedelta(days=1)
start_date = month_start.strftime('%Y-%m-%d')
end_date = today.strftime('%Y-%m-%d')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_accounts_emails_mapping():
    s3_client = boto3.client('s3')
    organizations_client = boto3.client('organizations', region_name='us-east-1')

    logging.info("Clients created")

    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=ACCOUNTS_MANAGERS_MAPPING_KEY)
    mapping_data = json.loads(response['Body'].read().decode('utf-8'))

    logging.info("Mapping data fetched")
    logging.debug(mapping_data)
    
    accounts_emails_mapping = []
    
    paginator = organizations_client.get_paginator('list_accounts_for_parent')
    logging.info("Paginator created")

    pages = paginator.paginate(
        ParentId=SANDBOX_OU_ID,
        PaginationConfig={
            'PageSize': 20
        }
    )

    logging.info("Fetched sandbox accounts list")

    for page in pages:
        logging.debug(page)
        for account in page['Accounts']:
            if account['Status'] == 'ACTIVE':
                accounts_emails_mapping.append(
                    {
                        "accountId" : account['Id'],
                        "email" : mapping_data[account['Id']]['managerEmail']
                    }
                )

    logging.info("Accounts emails mapping fetched")
    logging.debug(accounts_emails_mapping)
    return accounts_emails_mapping


def send_email(account_id, manager_email, actual_cost, actual_cost_unit):
    month = month_start.strftime("%B %Y")
    subject = f'AWS Cost Report for Account {account_id} - {month}'

    body_text = (
        f'Cost Report for AWS Account: {account_id}\n'
        f'Month: {month}\n\n'
        f'Current Cost (up to {end_date}): {actual_cost:.2f} {actual_cost_unit}\n'
        f'Click here to view the detailed cost report in AWS Cost Explorer.\n\n'
        f'This is an automated message. For details, check AWS Cost Explorer.'
    )

    body_html = (
        f"""
        <h2>Cost Report for AWS Account: {account_id}</h2>
        <p><strong>Month:</strong> {month}</p>
        <ul>
            <li><strong>Current Cost (up to {end_date}):</strong> {actual_cost:.2f} {actual_cost_unit}</li>
        </ul>
        <p>This is an automated message. For details, check <a href="https://us-east-1.console.aws.amazon.com/costmanagement/home?region=us-east-1#/home"><b> AWS Cost Explorer </b></a></p>
        """
    )
    
    ses_client = boto3.client('ses', region_name='us-east-1')
    ses_client.send_email(
        Source=SENDER_EMAIL,
        Destination={
            'ToAddresses': [manager_email]
        },
        Message={
            'Subject': {'Data': subject},
            'Body': {
                'Text': {'Data': body_text},
                'Html': {'Data': body_html}
            }
        }
    )

    logging.info(f'Email sent to {manager_email} for account {account_id}')
    

def lambda_handler(event, context):
    try:
        accounts_emails_mapping = get_accounts_emails_mapping()
        ce_client = boto3.client('ce', region_name='us-east-1')
        
        logging.debug(f'Start Date: {start_date}')
        logging.debug(f'End Date: {end_date}')

        for mapping in accounts_emails_mapping:
            account_id = mapping['accountId']
            manager_email = mapping['email']

            logging.debug(f'Account Id: {account_id}')
            logging.debug(f'Manager Email: {manager_email}')

            actual_response = ce_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Granularity='MONTHLY',
                Metrics=['UnblendedCost'],
                Filter={
                    'Dimensions': {
                        'Key': 'LINKED_ACCOUNT',
                        'Values': [account_id]
                    }
                }
            )

            logging.info(f"Successfully fetched current month costs for account {account_id}")
        
            actual_cost = float(actual_response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
            actual_cost_unit = actual_response['ResultsByTime'][0]['Total']['UnblendedCost']['Unit']

            logging.debug(actual_cost)
            
            send_email(account_id, manager_email, actual_cost, actual_cost_unit)       
        
        return {
            'statusCode': 200,
            'body': json.dumps('Emails sent successfully')
        }
        
    except ClientError as e:
        error_message = f'AWS Error: {e.response["Error"]["Message"]}'
        return {
            'statusCode': 500,
            'body': json.dumps(error_message)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }