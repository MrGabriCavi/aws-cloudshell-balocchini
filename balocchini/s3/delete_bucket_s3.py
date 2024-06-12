import boto3
import argparse
import sys
from botocore.exceptions import ProfileNotFound
from tqdm import tqdm

def count_objects(s3_client, bucket_name):
    """Conta tutti gli oggetti nel bucket, comprese le directory."""
    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name)
    
    object_count = 0
    for page in page_iterator:
        if 'Contents' in page:
            object_count += len(page['Contents'])
    return object_count

def delete_objects(s3_client, bucket_name):
    """Cancella tutti gli oggetti nel bucket, comprese le directory."""
    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name)
    
    # Conta tutti gli oggetti (comprese le directory)
    total_objects = count_objects(s3_client, bucket_name)

    with tqdm(total=total_objects, desc=f"Deleting objects in {bucket_name}") as pbar:
        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
                    pbar.update(1)

def delete_bucket(s3_client, bucket_name):
    """Cancella il bucket."""
    s3_client.delete_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' has been deleted.")

def main(target_bucket, profile):
    if profile:
        try:
            boto3.setup_default_session(profile_name=profile)
        except ProfileNotFound:
            print(f"Profile '{profile}' not found.")
            sys.exit(1)
    
    s3_client = boto3.client('s3')
    
    # Conta tutti gli oggetti nel bucket
    object_count = count_objects(s3_client, target_bucket)
    
    # Chiede conferma all'utente
    confirmation = input(f"The bucket '{target_bucket}' contains {object_count} objects. Do you really want to delete it? (y/n): ")
    if confirmation.lower() != 'y':
        print("Deletion cancelled.")
        return
    
    # Cancella tutti gli oggetti nel bucket
    delete_objects(s3_client, target_bucket)
    
    # Cancella il bucket
    delete_bucket(s3_client, target_bucket)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete an S3 bucket and all its contents.")
    parser.add_argument("--target", type=str, required=True, help="The name of the bucket to delete.")
    parser.add_argument("-p", "--profile", type=str, help="The AWS credentials profile to use.")
    
    args = parser.parse_args()
    
    main(args.target, args.profile)