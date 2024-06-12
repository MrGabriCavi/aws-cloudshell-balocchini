# balocchini/s3/operation.py

class S3Operation:
    def __init__(self, s3_common, s3_delete, s3_download):
        self.s3_common = s3_common
        self.s3_delete = s3_delete
        self.s3_download = s3_download

    def execute(self, operation, bucket=None, directory=None):
        if operation == 'list-buckets':
            self.list_buckets()
        elif operation == 'delete-bucket':
            self.delete_bucket(bucket)
        elif operation == 'download-bucket':
            self.download_bucket(bucket, directory)
        else:
            print("Operazione non riconosciuta. Usa 'list-buckets', 'delete-bucket' o 'download-bucket'.")

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

    def download_bucket(self, bucket, directory):
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

        self.s3_download.download_bucket(bucket, directory)