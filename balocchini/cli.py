import argparse
import os
from balocchini.session.session import create_session
from balocchini.s3.common import S3Common
from balocchini.s3.delete import S3Delete
from balocchini.s3.download import S3Download

def main():
    parser = argparse.ArgumentParser(description='Interfaccia a riga di comando per AWS.')
    parser.add_argument('--profile', type=str, help='Profilo AWS da utilizzare')
    parser.add_argument('--func', type=str, help='Funzionalità da eseguire')
    parser.add_argument('--op', type=str, help='Operazione da eseguire')
    parser.add_argument('--role-account', type=str, help='ID account AWS del ruolo da assumere')
    parser.add_argument('--role-sts', type=str, help='Nome del ruolo STS da assumere')
    parser.add_argument('--s3-bucket', type=str, help='Nome del bucket S3 da gestire')
    parser.add_argument('--s3-directory', type=str, help='Directory di destinazione per il download')
    args = parser.parse_args()

    session = create_session(args.profile, args.role_account, args.role_sts)

    if args.func:
        if args.func == 's3':
            s3_menu(session, args.op, args.s3_bucket, args.s3_directory)
        else:
            print("Funzionalità non riconosciuta. Usa 's3'.")
    else:
        main_menu(session)

def main_menu(session):
    while True:
        print("\nScegli una funzionalità:")
        print("1. s3")
        print("q. quit")
        choice = input("Inserisci il numero o il nome della funzionalità: ").strip().lower()

        if choice in ['1', 's3']:
            s3_menu(session)
        elif choice == 'q':
            print("Uscita dal programma.")
            break
        else:
            print("Scelta non valida. Riprova.")

def s3_menu(session, op=None, bucket=None, directory=None):
    s3_common = S3Common(session)
    s3_delete = S3Delete(session)
    s3_download = S3Download(session)
    if op:
        execute_s3_operation(s3_common, s3_delete, s3_download, op, bucket, directory)
        return

    while True:
        print("\nFunzionalità s3:")
        print("1. list-buckets")
        print("2. delete-bucket")
        print("3. download-bucket")
        print("q. torna-al-menu-principale")
        choice = input("Inserisci il numero o il nome dell'operazione: ").strip().lower()

        if choice in ['1', 'list-buckets']:
            execute_s3_operation(s3_common, s3_delete, s3_download, 'list-buckets')
        elif choice in ['2', 'delete-bucket']:
            execute_s3_operation(s3_common, s3_delete, s3_download, 'delete-bucket', bucket)
        elif choice in ['3', 'download-bucket']:
            execute_s3_operation(s3_common, s3_delete, s3_download, 'download-bucket', bucket, directory)
        elif choice == 'q':
            break
        else:
            print("Scelta non valida. Riprova.")

def execute_s3_operation(s3_common, s3_delete, s3_download, operation, bucket=None, directory=None):
    if operation == 'list-buckets':
        buckets = s3_common.list_buckets()
        print("\nElenco dei bucket S3:")
        for bucket in buckets:
            print(bucket)
    elif operation == 'delete-bucket':
        if not bucket:
            buckets = s3_common.list_buckets()
            print("\nScegli un bucket da cancellare:")
            for i, bucket_name in enumerate(buckets):
                print(f"{i + 1}. {bucket_name}")
            choice = input("Inserisci il numero del bucket da cancellare: ").strip()
            try:
                bucket = buckets[int(choice) - 1]
            except (IndexError, ValueError):
                print("Scelta non valida.")
                return

        object_count = s3_common.count_objects(bucket, ignore_folders=False)
        confirmation = input(f"The bucket '{bucket}' contains {object_count} objects. Do you really want to delete it? (y/n): ")
        if confirmation.lower() != 'y':
            print("Deletion cancelled.")
            return

        s3_delete.delete_objects(bucket, s3_common.count_objects)
        s3_delete.delete_bucket(bucket)
    elif operation == 'download-bucket':
        if not bucket:
            buckets = s3_common.list_buckets()
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

        s3_download.download_bucket(bucket, directory)
    else:
        print("Operazione non riconosciuta. Usa 'list-buckets', 'delete-bucket' o 'download-bucket'.")

if __name__ == "__main__":
    main()
