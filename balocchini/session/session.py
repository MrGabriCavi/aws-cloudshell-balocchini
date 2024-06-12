import boto3

def create_session(profile_name=None, role_account=None, role_sts=None):
    if profile_name:
        session = boto3.Session(profile_name=profile_name)
    else:
        session = boto3.Session()

    if role_account and role_sts:
        sts_client = session.client('sts')
        assumed_role = sts_client.assume_role(
            RoleArn=f"arn:aws:iam::{role_account}:role/{role_sts}",
            RoleSessionName="AssumeRoleSession"
        )
        credentials = assumed_role['Credentials']
        session = boto3.Session(
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

    return session