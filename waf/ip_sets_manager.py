import boto3
import argparse

def list_waf_ip_sets(scope):
    """
    Lista gli IP Set di AWS WAF e permette all'utente di selezionarne uno per visualizzarne i dettagli.

    :param scope: 'REGIONAL' per risorse regionali o 'CLOUDFRONT' per risorse associate a CloudFront.
    """
    wafv2_client = boto3.client('wafv2')

    try:
        response = wafv2_client.list_ip_sets(Scope=scope)
        ip_sets = response['IPSets']

        if not ip_sets:
            print("Nessun IP Set trovato.")
            return

        # Stampa gli IP set con un indice
        for index, ip_set in enumerate(ip_sets, start=1):
            print(f"{index}. Name: {ip_set['Name']}, ARN: {ip_set['ARN']}")

        # Chiede all'utente di selezionare un IP Set
        selection = int(input("Inserisci il numero dell'IP Set per visualizzarne i dettagli: ")) - 1

        if selection < 0 or selection >= len(ip_sets):
            print("Selezione non valida.")
            return

        # Recupera l'ID e l'ARN dell'IP Set selezionato
        ip_set_id = ip_sets[selection]['Id']
        ip_set_arn = ip_sets[selection]['ARN']

        # Recupera i dettagli dell'IP Set selezionato
        ip_set_details = wafv2_client.get_ip_set(
            Scope=scope,
            Id=ip_set_id,
            Name=ip_sets[selection]['Name']
        )

        print(f"Dettagli per {ip_sets[selection]['Name']}:")
        print(f"ARN: {ip_set_arn}")
        print("IP Addresses:")
        for address in ip_set_details['IPSet']['Addresses']:
            print(address)

    except Exception as e:
        print(f"Errore durante l'elenco o la selezione degli IP Set: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Lista gli IP Set di AWS WAF e permette la selezione per dettagli.')
    parser.add_argument('scope', type=str, choices=['REGIONAL', 'CLOUDFRONT'],
                        help='Lo scope degli IP Set da elencare.')
    args = parser.parse_args()
    list_waf_ip_sets(args.scope)