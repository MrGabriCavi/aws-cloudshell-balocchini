from prettytable import PrettyTable
from .common import S3Common

class S3TableInfo:
    def __init__(self, session):
        self.s3_common = S3Common(session)

    def print_table_info(self):
        buckets = self.s3_common.list_bucket_complete()
        table = PrettyTable()
        table.field_names = ["Bucket Name", "ARN", "Creation Date", "Encryption", "KMS Key ARN"]
        table.align["Bucket Name"] = "l"
        table.align["ARN"] = "l"
        table.align["Creation Date"] = "l"
        table.align["Encryption"] = "l"
        table.align["KMS Key ARN"] = "l"
        
        for bucket in buckets:
            name = bucket['Name']
            arn = f"arn:aws:s3:::{name}"
            creation_date = bucket['CreationDate']
            encryption, kms_key_arn = self.s3_common.get_bucket_encryption(name)
            table.add_row([name, arn, creation_date, encryption, kms_key_arn])
        
        print(table)