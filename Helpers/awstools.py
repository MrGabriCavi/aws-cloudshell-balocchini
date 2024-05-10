# Helpers/awstools.py

import boto3
from botocore.exceptions import ProfileNotFound

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