class S3Common:
    def __init__(self, session):
        self.s3 = session.client('s3')

    def list_buckets(self):
        response = self.s3.list_buckets()
        return [bucket['Name'] for bucket in response['Buckets']]