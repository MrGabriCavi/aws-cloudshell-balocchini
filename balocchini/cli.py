# balocchini/cli.py

import argparse
from balocchini.session.session import create_session
import balocchini.s3 as s3
import balocchini.ssm as ssm
from balocchini.s3.menu import S3Menu
from balocchini.ssm.menu import SSMMenu


def main():
    parser = argparse.ArgumentParser(description='Interfaccia a riga di comando per AWS.')
    # Argomenti generali
    parser.add_argument('--profile', type=str, help='Profilo AWS da utilizzare')
    parser.add_argument('--func', type=str, help='Funzionalità da eseguire')
    parser.add_argument('--op', type=str, help='Operazione da eseguire')
    parser.add_argument('--role-account', type=str, help='ID account AWS del ruolo da assumere')
    parser.add_argument('--role-sts', type=str, help='Nome del ruolo STS da assumere')

    # Caricamento degli argomenti specifici
    s3.load_arguments(parser)
    ssm.load_arguments(parser)

    args = parser.parse_args()

    session = create_session(args.profile, args.role_account, args.role_sts)

    if args.func:
        if args.func == 's3':
            s3_menu = S3Menu(session)
            s3_menu.display_menu(args.op, args.s3_bucket, args.s3_directory, args.s3_md_include, args.s3_md_exclude,
                                 args.s3_with_checksum_sha256)
        elif args.func == 'ssm':
            ssm_menu = SSMMenu(session, args.profile)
            ssm_menu.display_menu(args.ssm_i)
        else:
            print("Funzionalità non riconosciuta. Usa 's3' o 'ssm'.")
    else:
        main_menu(session)


def main_menu(session):
    while True:
        print("\nScegli una funzionalità:")
        print("1. s3")
        print("2. ssm")
        print("q. quit")
        choice = input("Inserisci il numero o il nome della funzionalità: ").strip().lower()

        if choice in ['1', 's3']:
            s3_menu = S3Menu(session)
            s3_menu.display_menu()
        elif choice in ['2', 'ssm']:
            ssm_menu = SSMMenu(session)
            ssm_menu.display_menu()
        elif choice == 'q':
            print("Uscita dal programma.")
            break
        else:
            print("Scelta non valida. Riprova.")


if __name__ == "__main__":
    main()