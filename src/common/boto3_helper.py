import boto3


def get_boto3_client(service, access_key=None, secret_access_key=None, session_token=None, region=None):
    client = boto3.client(
        service,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key,
        aws_session_token=session_token,
        region_name=region
    )
    return client