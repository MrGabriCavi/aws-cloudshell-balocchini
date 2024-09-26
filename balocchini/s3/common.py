class S3Common:
    def __init__(self, session):
        self.s3 = session.client('s3')
        self.s3control = session.client('s3control')
        self.sts = session.client('sts')

    def list_buckets(self):
        response = self.s3.list_buckets()
        return [bucket['Name'] for bucket in response['Buckets']]

    def list_bucket_complete(self):
        response = self.s3.list_buckets()
        return response['Buckets']

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

    def get_bucket_encryption(self, bucket_name):
        """Ottiene le informazioni di crittografia per un bucket."""
        try:
            response = self.s3.get_bucket_encryption(Bucket=bucket_name)
            rules = response.get('ServerSideEncryptionConfiguration', {}).get('Rules', [])
            if rules:
                for rule in rules:
                    if 'ApplyServerSideEncryptionByDefault' in rule:
                        sse_algorithm = rule['ApplyServerSideEncryptionByDefault'].get('SSEAlgorithm')
                        kms_key_arn = rule['ApplyServerSideEncryptionByDefault'].get('KMSMasterKeyID', 'N/A')
                        return sse_algorithm, kms_key_arn
            return 'None', 'N/A'
        except self.s3.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                return 'None', 'N/A'
            else:
                print(f"Errore nell'ottenere la crittografia del bucket: {e}")
                return 'Error', 'N/A'