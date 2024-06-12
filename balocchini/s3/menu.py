# balocchini/s3/menu.py

from .common import S3Common
from .delete import S3Delete
from .download import S3Download
from .operation import S3Operation

class S3Menu:
    def __init__(self, session):
        self.s3_common = S3Common(session)
        self.s3_delete = S3Delete(session)
        self.s3_download = S3Download(session)
        self.s3_operation = S3Operation(self.s3_common, self.s3_delete, self.s3_download)

    def display_menu(self, op=None, bucket=None, directory=None, include=None, exclude=None, with_checksum=None):
        if op:
            self.s3_operation.execute(op, bucket, directory, include, exclude, with_checksum)
            return

        while True:
            print("\nFunzionalità s3:")
            print("1. list-buckets")
            print("2. delete-bucket")
            print("3. download-bucket")
            print("4. download-multiple-buckets")
            print("q. torna-al-menu-principale")
            choice = input("Inserisci il numero o il nome dell'operazione: ").strip().lower()

            if choice in ['1', 'list-buckets']:
                self.s3_operation.execute('list-buckets')
            elif choice in ['2', 'delete-bucket']:
                self.s3_operation.execute('delete-bucket', bucket)
            elif choice in ['3', 'download-bucket']:
                self.s3_operation.execute('download-bucket', bucket, directory, with_checksum)
            elif choice in ['4', 'download-multiple-buckets']:
                self.s3_operation.execute('download-multiple-buckets', directory=directory, include=include, exclude=exclude, with_checksum=with_checksum)
            elif choice == 'q':
                break
            else:
                print("Scelta non valida. Riprova.")