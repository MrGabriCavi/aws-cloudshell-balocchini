import os
import sys
import hashlib
import shutil
import boto3
import tarfile
import argparse
from botocore.exceptions import ProfileNotFound
from tqdm import tqdm

MAX_FILENAME_LENGTH = 255  # Lunghezza massima del nome file

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def calculate_total_objects(page_iterator):
    counter = 0
    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                file_key = obj['Key']
                if not file_key.endswith('/'):
                    counter += 1
    return counter                
                    

def shorten_filename(file_key, max_length=MAX_FILENAME_LENGTH):
    if len(file_key) <= max_length:
        return file_key, None

    # Calcola un hash univoco per il file key
    hash_suffix = hashlib.md5(file_key.encode()).hexdigest()
    short_name = file_key[:max_length - len(hash_suffix) - 1] + '_' + hash_suffix
    return short_name, file_key

def download_bucket(s3_client, bucket_name, target_dir):
    bucket_dir = os.path.join(target_dir, bucket_name)
    os.makedirs(bucket_dir, exist_ok=True)
    
    sha256_file_path = os.path.join(target_dir, f"{bucket_name}.sha256")
    with open(sha256_file_path, 'w') as sha256_file, open(os.path.join(target_dir, f"{bucket_name}_filenames.txt"), 'w') as filename_map_file:
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name)
        
        total_objects = calculate_total_objects(page_iterator)       
        
        page_iterator = paginator.paginate(Bucket=bucket_name)  # Reset iterator

        with tqdm(total=total_objects, desc=f"Downloading {bucket_name}") as download_pbar:
            for page in page_iterator:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        file_key = obj['Key']
                        short_file_key, original_file_key = shorten_filename(file_key)
                        target_file_path = os.path.join(bucket_dir, short_file_key)
                        
                        # Verifica se l'oggetto è una directory
                        if file_key.endswith('/'):
                            os.makedirs(target_file_path, exist_ok=True)
                        else:
                            os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
                            s3_client.download_file(bucket_name, file_key, target_file_path)
                            download_pbar.update(1)
                            
                            # Scrivi la mappatura dei nomi dei file se accorciati
                            if original_file_key:
                                filename_map_file.write(f"{short_file_key} -> {original_file_key}\n")
        
        # Calcolo degli SHA256 con barra di avanzamento
        with tqdm(total=total_objects, desc=f"Calculating SHA256 for {bucket_name}") as sha256_pbar:
            for page in page_iterator:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        file_key = obj['Key']
                        short_file_key, original_file_key = shorten_filename(file_key)
                        target_file_path = os.path.join(bucket_dir, short_file_key)
                        
                        if not file_key.endswith('/'):
                            file_sha256 = calculate_sha256(target_file_path)
                            sha256_file.write(f"{file_sha256}  {os.path.join(bucket_name, short_file_key)}\n")
                            sha256_pbar.update(1)
    
    return bucket_dir, sha256_file_path

def create_tar_gz(target_dir, bucket_name, bucket_dir, sha256_file_path):
    tar_gz_path = os.path.join(target_dir, f"{bucket_name}.tar.gz")
    with tarfile.open(tar_gz_path, "w:gz") as tar:
        tar.add(bucket_dir, arcname=bucket_name)
        tar.add(sha256_file_path, arcname=os.path.basename(sha256_file_path))
    return tar_gz_path

def main(target_dir, excluded_buckets, profile):
    if profile:
        try:
            boto3.setup_default_session(profile_name=profile)
        except ProfileNotFound:
            print(f"Profile '{profile}' not found.")
            sys.exit(1)
    
    s3_client = boto3.client('s3')
    buckets = s3_client.list_buckets()['Buckets']
    
    for bucket in buckets:
        bucket_name = bucket['Name']
        if bucket_name in excluded_buckets:
            print(f"Skipping excluded bucket: {bucket_name}")
            continue
        
        print(f"Processing bucket: {bucket_name}")
        bucket_dir, sha256_file_path = download_bucket(s3_client, bucket_name, target_dir)
        tar_gz_path = create_tar_gz(target_dir, bucket_name, bucket_dir, sha256_file_path)
        print(f"Created tar.gz archive: {tar_gz_path}")
        
        # Creazione della directory finale
        final_dir = os.path.join(target_dir, f"{bucket_name}_final")
        os.makedirs(final_dir, exist_ok=True)
        
        # Rinominare e spostare la directory del bucket
        final_bucket_dir = os.path.join(final_dir, "bucket_content")
        shutil.move(bucket_dir, final_bucket_dir)
        
        # Spostare il file .sha256
        final_sha256_file_path = os.path.join(final_dir, os.path.basename(sha256_file_path))
        shutil.move(sha256_file_path, final_sha256_file_path)
        
        # Spostare il file .tar.gz
        final_tar_gz_path = os.path.join(final_dir, os.path.basename(tar_gz_path))
        shutil.move(tar_gz_path, final_tar_gz_path)
        
        # Spostare il file di mappatura dei nomi
        final_filename_map_file_path = os.path.join(final_dir, f"{bucket_name}_filenames.txt")
        shutil.move(os.path.join(target_dir, f"{bucket_name}_filenames.txt"), final_filename_map_file_path)
        
        print(f"Final directory created: {final_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download S3 buckets and create tar.gz archives with SHA256 checksums.")
    parser.add_argument("target_directory", type=str, help="The target directory where the buckets will be downloaded and archived.")
    parser.add_argument("excluded_buckets", nargs="*", help="List of buckets to exclude from the download.")
    parser.add_argument("-p", "--profile", type=str, help="The AWS credentials profile to use.")
    
    args = parser.parse_args()
    
    main(args.target_directory, args.excluded_buckets, args.profile)