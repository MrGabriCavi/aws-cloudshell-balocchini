# balocchini/cli.py

import argparse
from balocchini.session.session import create_session
from balocchini.s3.common import S3Common

def main():
    parser = argparse.ArgumentParser(description='Interfaccia a riga di comando per AWS.')
    parser.add_argument('--profile', type=str, help='Profilo AWS da utilizzare')
    parser.add_argument('--func', type=str, help='Funzionalità da eseguire')
    parser.add_argument('--op', type=str, help='Operazione da eseguire')
    parser.add_argument('--role-account', type=str, help='ID account AWS del ruolo da assumere')
    parser.add_argument('--role-sts', type=str, help='Nome del ruolo STS da assumere')
    args = parser.parse_args()

    session = create_session(args.profile, args.role_account, args.role_sts)

    if args.func:
        if args.func == 's3':
            s3_menu(session, args.op)
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

def s3_menu(session, op=None):
    s3_common = S3Common(session)
    if op:
        execute_s3_operation(s3_common, op)
        return

    while True:
        print("\nFunzionalità s3:")
        print("1. list-buckets")
        print("q. torna-al-menu-principale")
        choice = input("Inserisci il numero o il nome dell'operazione: ").strip().lower()

        if choice in ['1', 'list-buckets']:
            execute_s3_operation(s3_common, 'list-buckets')
        elif choice == 'q':
            break
        else:
            print("Scelta non valida. Riprova.")

def execute_s3_operation(s3_common, operation):
    if operation == 'list-buckets':
        buckets = s3_common.list_buckets()
        print("\nElenco dei bucket S3:")
        for bucket in buckets:
            print(bucket)
    else:
        print("Operazione non riconosciuta. Usa 'list-buckets'.")

if __name__ == "__main__":
    main()