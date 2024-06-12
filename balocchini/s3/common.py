class S3Common:
    def __init__(self, session):
        self.s3 = session.client('s3')

    def list_buckets(self):
        response = self.s3.list_buckets()
        return [bucket['Name'] for bucket in response['Buckets']]

    def count_objects(self, bucket_name, ignore_folders=True):
        """Conta tutti gli oggetti nel bucket. Se ignore_folders è True, non conta le directory."""
        paginator = self.s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name)

        object_count = 0
        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    if ignore_folders and obj['Key'].endswith('/'):
                        continue
                    object_count += 1
        return object_count
