import sys
import os
# Aggiungi il percorso della directory superiore a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import boto3

def assume_role(role_arn, session_name):
    """
    Assumes a role using STS and returns a session.
    """
    sts_client = boto3.client('sts')
    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=session_name
    )
    credentials = response['Credentials']
    session = boto3.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )
    return session

def change_cname_record(hosted_zone_id, record_name, new_cname, credentials):
    """
    Changes the CNAME record of the specified hosted zone.
    """
    route53_client = boto3.client('route53', 
                                  aws_access_key_id=credentials['AccessKeyId'],
                                  aws_secret_access_key=credentials['SecretAccessKey'],
                                  aws_session_token=credentials['SessionToken'])
    response = route53_client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': record_name,
                        'Type': 'CNAME',
                        'TTL': 300,
                        'ResourceRecords': [
                            {
                                'Value': new_cname
                            }
                        ]
                    }
                }
            ]
        }
    )
    print("CNAME record changed successfully.")

def change_cloudfront_alternate_domain(cf_distribution_id, new_domain_name, credentials):
    """
    Changes the alternate domain name of the specified CloudFront distribution.
    """
    cloudfront_client = boto3.client('cloudfront',
                                     aws_access_key_id=credentials['AccessKeyId'],
                                     aws_secret_access_key=credentials['SecretAccessKey'],
                                     aws_session_token=credentials['SessionToken'])
    response = cloudfront_client.update_distribution(
        DistributionConfig={
            'Id': cf_distribution_id,
            'Aliases': {
                'Quantity': 1,
                'Items': [
                    new_domain_name
                ]
            }
        },
        IfMatch=response['ETag']
    )
    print("CloudFront alternate domain name changed successfully.")

def main():
    role_arn = input("Select yout role arn: ")  # Specify the role ARN to assume
    session_name = input("Select your session name: ")  # Specify a name for the assumed session
    
    # Assume the role
    assumed_session = assume_role(role_arn, session_name)
    
    
    hosted_zone_id = input("Select your hosted zone id: ") # Specify the hosted zone ID
    record_name = input("Select your record name: ")  # Specify the record name
    new_cname = input("Select your new record name: ")  # Specify the new CNAME value
    
    # Change the CNAME record using the assumed session
    change_cname_record(hosted_zone_id, record_name, new_cname, assumed_session.get_credentials())
    
    
    cf_distribution_id = input("Select your CF id: ")  # Specify the CloudFront distribution ID
    new_domain_name = input("Select domain name: ") # Specify the new alternate domain name for CloudFront

    # Change the alternate domain name of CloudFront using the assumed session
    change_cloudfront_alternate_domain(cf_distribution_id, new_domain_name,assumed_session.get_credentials())


    hosted_zone_id_2 = input("Select your hosted zone id: ") # Specify the hosted zone ID
    record_name_2 = input("Select your record name: ")  # Specify the record name
    new_cname_2 = input("Select your new record name: ")  # Specify the new CNAME value
    
    # Change the CNAME record using the assumed session
    change_cname_record(hosted_zone_id_2, record_name_2, new_cname_2, assumed_session.get_credentials())
    
    cf_distribution_id_2 = input("Select your CF id: ")  # Specify the CloudFront distribution ID
    new_domain_name_2 = input("Select domain name: ") # Specify the new alternate domain name for CloudFront
    
    # Change the alternate domain name of CloudFront using the assumed session
    change_cloudfront_alternate_domain(cf_distribution_id_2, new_domain_name_2,assumed_session.get_credentials())

if __name__ == "__main__":
    main()




