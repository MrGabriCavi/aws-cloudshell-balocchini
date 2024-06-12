import boto3
import argparse
import sys
import os

# Aggiungi il percorso della directory superiore a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Helpers.awstools import AWSTools

def list_buckets(s3_client):
    response = s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    return buckets

def navigate_bucket(s3_client, bucket_name, prefix=''):
    paginator = s3_client.get_paginator('list_objects_v2')
    operation_parameters = {'Bucket': bucket_name, 'Prefix': prefix, 'Delimiter': '/'}
    page_iterator = paginator.paginate(**operation_parameters)

    print(f"\nContenuti del bucket '{bucket_name}' con prefisso '{prefix}':")
    for page in page_iterator:
        if 'CommonPrefixes' in page:
            for prefix in page['CommonPrefixes']:
                print(f"D: {prefix['Prefix']}")
        if 'Contents' in page:
            for obj in page['Contents']:
                print(f"F: {obj['Key']}")

def main():
    parser = argparse.ArgumentParser(description='Naviga e scarica da bucket S3.')
    parser.add_argument('--profile', type=str, help='Il nome del profilo AWS da utilizzare.', default=None)
    args = parser.parse_args()

    s3_client = s3_client = AWSTools.initialize_client('s3', args.profile, region='us-east-1')
    buckets = list_buckets(s3_client)

    while True:
        print("\nBucket disponibili:")
        for idx, bucket in enumerate(buckets, start=1):
            print(f"{idx}. {bucket}")
        print("q. Esci")

        bucket_choice = input("Seleziona un bucket per elencarne il contenuto o 'q' per uscire: ").strip()
        if bucket_choice.lower() == 'q':
            print("Bye")
            break

        try:
            bucket_idx = int(bucket_choice) - 1
            if 0 <= bucket_idx < len(buckets):
                current_prefix = ''
                while True:
                    contents = AWSTools.list_bucket_contents(s3_client, bucket_name, current_prefix)
                    print("\n0. Torna indietro")
                    print("00. Scarica tutto")
                    for i, item in enumerate(contents, start=1):
                        print(f"{i}. {'D' if item.endswith('/') else 'F'}: {item}")

                    choice = input("Seleziona un'opzione: ").strip()
                    if choice == '0':
                        if current_prefix == '':
                            break  # Torna alla selezione del bucket
                        current_prefix = '/'.join(current_prefix.split('/')[:-2]) + '/'
                        continue
                    elif choice == '00':
                        destination = input("Inserisci la directory di destinazione: ").strip()
                        AWSTools.download_directory(s3_client, bucket_name, current_prefix, destination)
                        continue

                    try:
                        choice_idx = int(choice) - 1
                        if 0 <= choice_idx < len(contents):
                            selected_item = contents[choice_idx]
                            if selected_item.endswith('/'):
                                current_prefix = selected_item
                            else:
                                destination = input("Inserisci la directory di destinazione per il file: ").strip()
                                AWSTools.download_file(s3_client, bucket_name, selected_item, os.path.join(destination, selected_item.split('/')[-1]))
                    except ValueError:
                        print("Selezione non valida.")
            else:
                print("Selezione non valida.")
        except ValueError:
            print("Inserisci un numero valido o 'q' per uscire.")

if __name__ == "__main__":
    main()