import os
import boto3
from botocore.exceptions import ClientError, ProfileNotFound

class AWSTools:
    @staticmethod
    def verify_region(region, profile=None):
        """Checks if a given region exists in AWS, using a specific profile if provided."""
        try:
            if profile:
                session = boto3.Session(profile_name=profile)
            else:
                session = boto3.Session()
                
            ec2_client = session.client('ec2', region_name=region)
            
            response = ec2_client.describe_regions()
            regions = [region['RegionName'] for region in response['Regions']]
            return region in regions
        except ProfileNotFound as e:
            print(f"Profile '{profile}' not found. Make sure the profile is configured correctly.")
            return False
        except Exception as e:
            print(f"Error during region verification: {e}")
            return False
        
    @staticmethod
    def initialize_client(service, profile=None, region=None, role_arn=None):
        """Initializes and returns a boto3 client for a specified AWS service, optionally using a specified profile, region, and role."""
        try:
            if profile:
                session = boto3.Session(profile_name=profile)
            else:
                session = boto3.Session()
                
            if role_arn:
                sts_client = session.client('sts')
                assumed_role = sts_client.assume_role(RoleArn=role_arn, RoleSessionName="AssumedRoleSession")
                credentials = assumed_role['Credentials']
                
                session = boto3.Session(
                    aws_access_key_id=credentials['AccessKeyId'],
                    aws_secret_access_key=credentials['SecretAccessKey'],
                    aws_session_token=credentials['SessionToken'],
                    region_name=region
                )
            
            client = session.client(service, region_name=region)
            return client
        except ProfileNotFound:
            print(f"Profilo '{profile}' non trovato. Assicurati che il profilo sia configurato correttamente.")
            exit()
        except ClientError as e:
            print(f"Errore durante l'inizializzazione del client: {e}")
            exit()
