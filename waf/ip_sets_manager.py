import sys
import os
# Aggiungi il percorso della directory superiore a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import boto3
import argparse
from prettytable import PrettyTable
from botocore.exceptions import ProfileNotFound
from Helpers.awstools import AWSTools

def initialize_client(service, profile, region, scope):
    try:
        session = boto3.Session(profile_name=profile) if profile else boto3.Session()
        # Se lo scope è CLOUDFRONT, utilizza una regione specifica per CloudFront, altrimenti usa la regione fornita
        selected_region = 'us-east-1' if scope == 'CLOUDFRONT' else region
        return session.client(service, region_name=selected_region)
    except ProfileNotFound:
        print(f"Profilo '{profile}' non trovato. Assicurati che il profilo sia configurato correttamente.")
        exit()

def is_ip_in_set(ip, ip_set_details):
    """Controlla se un IP è presente nell'IP Set."""
    return ip in ip_set_details['IPSet']['Addresses']

def create_ip_set(client, scope, name, addresses, description):
    try:
        response = client.create_ip_set(
            Name=name,
            Scope=scope,
            IPAddressVersion='IPV4',
            Addresses=[addr.strip() for addr in addresses.split(',')],  # Assicura che gli indirizzi siano ben formati
            Description=description
        )
        print(f"IP Set creato con successo. ARN: {response['Summary']['ARN']}")
    except Exception as e:
        print(f"Errore durante la creazione dell'IP Set: {e}")

def list_and_select_ip_set(client, scope):
    try:
        response = client.list_ip_sets(Scope=scope)
        ip_sets = response['IPSets']

        if not ip_sets:
            print("Nessun IP Set trovato.")
            return None

        for index, ip_set in enumerate(ip_sets, start=1):
            print(f"{index}. Name: {ip_set['Name']}, ARN: {ip_set['ARN']}")

        selection = int(input("Inserisci il numero dell'IP Set per visualizzarne i dettagli, 0 per tornare: ")) - 1

        if selection == -1:
            return None
        elif 0 <= selection < len(ip_sets):
            selected_ip_set = ip_sets[selection]
            ip_set_details = client.get_ip_set(Scope=scope, Id=selected_ip_set['Id'], Name=selected_ip_set['Name'])

            # Crea una tabella per visualizzare i dettagli
            table = PrettyTable()
            table.field_names = ["IP", "Description"]
            for address in ip_set_details['IPSet']['Addresses']:
                table.add_row([address, ip_set_details['IPSet'].get('Description', 'N/A')])

            print(table)
            return selected_ip_set
        else:
            print("Selezione non valida.")
            return None

    except Exception as e:
        print(f"Errore durante l'elenco o la selezione degli IP Set: {e}")
        return None

def update_ip_set(client, ip_set, ips, scope, action):
    try:
        # Recupera gli indirizzi IP correnti dell'IP Set selezionato e il LockToken
        response = client.get_ip_set(Scope=scope, Id=ip_set['Id'], Name=ip_set['Name'])
        current_ips = response['IPSet']['Addresses']
        lock_token = response['LockToken']

        updated_ips = current_ips[:]  # Crea una copia della lista degli indirizzi IP correnti

        if action == 'a':
            new_ips = [ip.strip() for ip in ips.split(',')]
            for ip in new_ips:
                if not is_ip_in_set(ip, response):
                    updated_ips.append(ip)
                else:
                    print(f"L'IP {ip} è già presente nell'IP Set.")
        elif action == 'r':
            ips_to_remove = [ip.strip() for ip in ips.split(',')]
            for ip in ips_to_remove:
                if is_ip_in_set(ip, response):
                    updated_ips.remove(ip)
            else:
                print(f"L'IP {ip} non è presente nell'IP Set e non può essere rimosso.")



        # Prepara i parametri per l'aggiornamento
        update_params = {
            'Name': ip_set['Name'],
            'Scope': scope,
            'Id': ip_set['Id'],
            'Addresses': updated_ips,
            'LockToken': lock_token,
        }

        # Aggiorna l'IP Set con la nuova lista di indirizzi IP
        client.update_ip_set(**update_params)
        print(f"IP Set '{ip_set['Name']}' aggiornato con successo.")
    except Exception as e:
        print(f"Errore durante l'aggiornamento dell'IP Set: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gestisci gli IP Set di AWS WAF.')
    parser.add_argument('scope', type=str, choices=['REGIONAL', 'CLOUDFRONT'], help='Lo scope degli IP Set da gestire.')
    parser.add_argument('--profile', type=str, help='Il nome del profilo AWS da utilizzare per le credenziali.', default=None)
    
    # Aggiungi un'opzione per la selezione della regione
    parser.add_argument('--region', type=str, help='La regione AWS da utilizzare.', default=None)
    
    args = parser.parse_args()

    # Chiedi all'utente di selezionare una regione se non specificata come argomento
     # Utilizza AWSTools per verificare la regione
    regioni_predefinite = ['eu-central-1', 'us-west-1', 'eu-south-1']
    
    if not args.region:
        print("Seleziona una regione dall'elenco seguente o inserisci il nome di una regione.")
        for i, regione in enumerate(regioni_predefinite, start=1):
            print(f"{i}. {regione}")
        print(f"{len(regioni_predefinite) + 1}. Inserisci una regione manualmente.")
        
        scelta = input("Inserisci il numero della tua scelta: ").strip()
        
        try:
            scelta_numerica = int(scelta)
            if 1 <= scelta_numerica <= len(regioni_predefinite):
                args.region = regioni_predefinite[scelta_numerica - 1]
            elif scelta_numerica == len(regioni_predefinite) + 1:
                regione_manuale = input("Inserisci il nome della regione: ").strip()
                if AWSTools.verify_region(regione_manuale, args.profile):
                    args.region = regione_manuale
                else:
                    print(f"La regione '{regione_manuale}' non è valida. Riprova.")
                    exit()
            else:
                print("Scelta non valida.")
                exit()
        except ValueError:
            print("Inserisci un numero valido.")
            exit()
        
        print(f"Regione selezionata: {args.region}")
    
    client = initialize_client('wafv2', args.profile, args.region, args.scope)

    try:
        while True:
            choice = input("Vuoi creare un nuovo IP Set (C), modificare un IP Set esistente (M), o uscire (Q/exit)? [C/M/Q]: ").upper()
            if choice == 'C':
                name = input("Inserisci il nome del nuovo IP Set: ")
                addresses = input("Inserisci gli indirizzi IP da includere nell'IP Set, separati da virgola: ")
                if addresses.lower() == 'exit':
                    print("Operazione annullata.")
                    continue
                if not addresses.strip():
                    print("L'elenco degli indirizzi IP non può essere vuoto.")
                    continue
                description = input("Inserisci una descrizione per l'IP Set: ")
                create_ip_set(client, args.scope, name, addresses, description)
            elif choice == 'M':
                selected_ip_set = list_and_select_ip_set(client, args.scope)
                if selected_ip_set:
                    while True:  # Aggiungi un ciclo per permettere all'utente di riprovare o uscire
                        action = input("Vuoi aggiungere (A) o rimuovere (R) IP, o uscire (exit)? [A/R/Q]: ").lower()
                        if action == 'q':
                            print("Operazione annullata.")
                            break  # Esce dal ciclo while, tornando al menu principale
                        elif action not in ['a', 'r']:
                            print("Scelta non valida. Inserisci 'A' per aggiungere, 'R' per rimuovere, o 'exit' per annullare.")
                            continue  # Dà all'utente un'altra possibilità di fare una scelta

                        ips = input("Inserisci gli IP separati da virgola: ")
                        if not ips.strip():
                            print("L'elenco degli indirizzi IP non può essere vuoto.")
                            continue  # Permette all'utente di inserire nuovamente gli IP

                        update_ip_set(client, selected_ip_set, ips, args.scope, action)
                        break  # Esce dal ciclo while dopo l'aggiornamento
            elif choice in ['Q', 'EXIT']:
                print("Bye!")
                break
            else:
                print("Scelta non valida.")
    except EOFError:
        print("\nBye!")  # Gestisce l'uscita con Ctrl+D