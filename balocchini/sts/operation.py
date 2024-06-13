# balocchini/sts/sts_operation.py

import boto3
import configparser
import os

class STSOperation:
    def __init__(self, session):
        self.sts = session.client('sts')

    def assume_role(self, role_arn, role_session_name):
        """Assume il ruolo specificato e restituisce le credenziali temporanee."""
        response = self.sts.assume_role(
            RoleArn=role_arn,
            RoleSessionName=role_session_name
        )
        return response['Credentials']

    def update_profile(self, profile_name, credentials):
        """Aggiorna il profilo nelle credenziali della macchina di esecuzione."""
        config = configparser.ConfigParser()
        credentials_file = os.path.expanduser('~/.aws/credentials')
        config.read(credentials_file)

        if profile_name not in config.sections():
            config.add_section(profile_name)

        config[profile_name]['aws_access_key_id'] = credentials['AccessKeyId']
        config[profile_name]['aws_secret_access_key'] = credentials['SecretAccessKey']
        config[profile_name]['aws_session_token'] = credentials['SessionToken']

        with open(credentials_file, 'w') as configfile:
            config.write(configfile)

        print(f"Profilo '{profile_name}' aggiornato con successo.")