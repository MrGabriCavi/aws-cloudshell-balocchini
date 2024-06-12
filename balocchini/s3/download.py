import os
from tqdm import tqdm
from balocchini.s3.common import S3Common

class S3Download:
    def __init__(self, session):
        self.s3 = session.client('s3')
        self.s3_common = S3Common(session)  # Crea un'istanza di S3Common

    def download_bucket(self, bucket_name, destination_directory):
        """Scarica tutti gli oggetti nel bucket nella directory di destinazione."""
        paginator = self.s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name)

        total_objects = self.s3_common.count_objects(bucket_name, ignore_folders=True)
        page_iterator = paginator.paginate(Bucket=bucket_name)  # Reset iterator

        with tqdm(total=total_objects, desc=f"Downloading objects from {bucket_name}") as pbar:
            for page in page_iterator:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        dest_path = os.path.join(destination_directory, key)
                        if key.endswith('/'):
                            os.makedirs(dest_path, exist_ok=True)
                        else:
                            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                            self.s3.download_file(bucket_name, key, dest_path)
                        pbar.update(1)