# Helpers/awstools.py

import os
import boto3
from botocore.exceptions import ClientError

class AWSTools:
    @staticmethod
    def verify_region(region, profile=None):
        """Checks if a given region exists in AWS, using a specific profile if provided."""
        try:
            # Crea una sessione utilizzando il profilo specificato, se fornito
            if profile:
                session = boto3.Session(profile_name=profile)
            else:
                session = boto3.Session()
                
            ec2_client = session.client('ec2', region_name='us-east-1')
            
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
    def initialize_client(service, profile=None, region=None):
        try:
            session = boto3.Session(profile_name=profile) if profile else boto3.Session()
            client = session.client(service, region_name=region)
            return client
        except ProfileNotFound:
            print(f"Profilo '{profile}' non trovato. Assicurati che il profilo sia configurato correttamente.")
            exit()
    
    @staticmethod
    def download_file(s3_client, bucket_name, object_name, destination):
        """Download a single file from S3."""
        try:
            s3_client.download_file(bucket_name, object_name, destination)
            print(f"File scaricato: {destination}")
        except ClientError as e:
            print(f"Errore durante il download: {e}")

    @staticmethod
    def download_directory(s3_client, bucket_name, prefix, destination):
        """Download the contents of a directory (prefix) recursively."""
        paginator = s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
            for obj in page.get('Contents', []):
                dest_path = os.path.join(destination, obj['Key'])
                if not os.path.exists(os.path.dirname(dest_path)):
                    os.makedirs(os.path.dirname(dest_path))
                s3_client.download_file(bucket_name, obj['Key'], dest_path)
        print(f"Contenuti di '{prefix}' scaricati in '{destination}'")        