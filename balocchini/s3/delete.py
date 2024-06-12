from tqdm import tqdm

class S3Delete:
    def __init__(self, session):
        self.s3 = session.client('s3')

    def delete_objects(self, bucket_name, count_objects_func):
        """Cancella tutti gli oggetti nel bucket, comprese le directory."""
        paginator = self.s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name)

        # Conta tutti gli oggetti (comprese le directory)
        total_objects = count_objects_func(bucket_name, ignore_folders=False)

        with tqdm(total=total_objects, desc=f"Deleting objects in {bucket_name}") as pbar:
            for page in page_iterator:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        self.s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                        pbar.update(1)

    def delete_bucket(self, bucket_name):
        """Cancella il bucket."""
        self.s3.delete_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' has been deleted.")