# balocchini/s3/operation.py

import os
import hashlib

class S3Operation:
    def __init__(self, s3_common, s3_delete, s3_download):
        self.s3_common = s3_common
        self.s3_delete = s3_delete
        self.s3_download = s3_download

    def execute(self, operation, bucket=None, directory=None, include=None, exclude=None, with_checksum=None):
        if operation == 'list-buckets':
            self.list_buckets()
        elif operation == 'delete-bucket':
            self.delete_bucket(bucket)
        elif operation == 'download-bucket':
            self.download_bucket(bucket, directory, with_checksum)
        elif operation == 'download-multiple-buckets':
            self.download_multiple_buckets(directory, include, exclude, with_checksum)
        else:
            print("Operazione non riconosciuta. Usa 'list-buckets', 'delete-bucket', 'download-bucket' o 'download-multiple-buckets'.")

    def list_buckets(self):
        buckets = self.s3_common.list_buckets()
        print("\nElenco dei bucket S3:")
        for bucket in buckets:
            print(bucket)

    def delete_bucket(self, bucket):
        if not bucket:
            buckets = self.s3_common.list_buckets()
            print("\nScegli un bucket da cancellare:")
            for i, bucket_name in enumerate(buckets):
                print(f"{i + 1}. {bucket_name}")
            choice = input("Inserisci il numero del bucket da cancellare: ").strip()
            try:
                bucket = buckets[int(choice) - 1]
            except (IndexError, ValueError):
                print("Scelta non valida.")
                return

        object_count = self.s3_common.count_objects(bucket, ignore_folders=False)
        confirmation = input(f"The bucket '{bucket}' contains {object_count} objects. Do you really want to delete it? (y/n): ")
        if confirmation.lower() != 'y':
            print("Deletion cancelled.")
            return

        self.s3_delete.delete_objects(bucket, self.s3_common.count_objects)
        self.s3_delete.delete_bucket(bucket)

    def download_bucket(self, bucket, directory, with_checksum):
        if not bucket:
            buckets = self.s3_common.list_buckets()
            print("\nScegli un bucket da scaricare:")
            for i, bucket_name in enumerate(buckets):
                print(f"{i + 1}. {bucket_name}")
            choice = input("Inserisci il numero del bucket da scaricare: ").strip()
            try:
                bucket = buckets[int(choice) - 1]
            except (IndexError, ValueError):
                print("Scelta non valida.")
                return

        if not directory:
            directory = input("Inserisci la directory di destinazione per il download: ").strip()
            if not os.path.isdir(directory):
                print("Directory non valida.")
                return

        if with_checksum is None:
            checksum_choice = input("Vuoi generare le checksum SHA-256? (y/n): ").strip().lower()
            with_checksum = checksum_choice == 'y'

        bucket_directory = os.path.join(directory, bucket)
        os.makedirs(bucket_directory, exist_ok=True)

        if with_checksum:
            objects_directory = os.path.join(bucket_directory, 'objects')
            os.makedirs(objects_directory, exist_ok=True)
            checksum_file_path = os.path.join(bucket_directory, f'{bucket}.sha256')
            with open(checksum_file_path, 'w') as checksum_file:
                self.s3_download.download_bucket(bucket, objects_directory, checksum_file)
        else:
            self.s3_download.download_bucket(bucket, bucket_directory)

    def download_multiple_buckets(self, directory, include=None, exclude=None, with_checksum=None):
        buckets = self.s3_common.list_buckets()

        if include:
            selected_buckets = [bucket for bucket in buckets if bucket in include]
        elif exclude:
            selected_buckets = [bucket for bucket in buckets if bucket not in exclude]
        else:
            print("\nScegli i bucket da scaricare (numeri separati da virgola):")
            for i, bucket_name in enumerate(buckets):
                print(f"{i + 1}. {bucket_name}")
            choices = input("Inserisci i numeri dei bucket da scaricare: ").strip()
            try:
                selected_buckets = [buckets[int(choice) - 1] for choice in choices.split(',')]
            except (IndexError, ValueError):
                print("Scelta non valida.")
                return

        for bucket in selected_buckets:
            print(f"Scaricamento del bucket: {bucket}")
            self.download_bucket(bucket, directory, with_checksum)