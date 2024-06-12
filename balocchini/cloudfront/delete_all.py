import boto3
import json
import subprocess
import argparse

def list_distributions(client):
    distributions = []
    paginator = client.get_paginator('list_distributions')
    for page in paginator.paginate():
        distributions.extend(page['DistributionList']['Items'])
    return distributions

def get_distribution_etag(client, distribution_id):
    response = client.get_distribution_config(Id=distribution_id)
    return response['ETag'], response['DistributionConfig']

def disable_distribution(client, distribution_id, etag, config):
    config['Enabled'] = False
    response = client.update_distribution(
        DistributionConfig=config,
        Id=distribution_id,
        IfMatch=etag
    )
    return response['ETag']

def delete_distribution(client, distribution_id, etag):
    client.delete_distribution(
        Id=distribution_id,
        IfMatch=etag
    )

def main(profile):
    session = boto3.Session(profile_name=profile)
    client = session.client('cloudfront')

    distributions = list_distributions(client)
    for distribution in distributions:
        distribution_id = distribution['Id']
        print(f"Disabling and deleting distribution with ID: {distribution_id}")

        etag, config = get_distribution_etag(client, distribution_id)
        etag = disable_distribution(client, distribution_id, etag, config)

        # Wait for distribution to be disabled
        waiter = client.get_waiter('distribution_deployed')
        waiter.wait(Id=distribution_id)
        
        delete_distribution(client, distribution_id, etag)
        print(f"Distribution with ID: {distribution_id} has been deleted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Delete all CloudFront distributions.')
    parser.add_argument('--profile', required=True, help='AWS CLI profile name')
    args = parser.parse_args()
    main(args.profile)
