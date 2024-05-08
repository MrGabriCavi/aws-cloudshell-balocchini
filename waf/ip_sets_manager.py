import boto3
import argparse

def list_waf_ip_sets(scope):
    """
    Lista gli IP Set di AWS WAF.

    :param scope: 'REGIONAL' per risorse regionali o 'CLOUDFRONT' per risorse associate a CloudFront.
    """
    # Crea un client WAFV2 utilizzando Boto3
    wafv2_client = boto3.client('wafv2')

    try:
        # Inizializza un array vuoto per raccogliere gli IP set
        ip_sets = []

        # Chiama l'API ListIPSets di WAFV2
        response = wafv2_client.list_ip_sets(Scope=scope)

        # Estrai gli IP set dalla risposta e aggiungili all'array
        ip_sets.extend(response['IPSets'])

        # Stampa gli IP set trovati
        for ip_set in ip_sets:
            print(f"ID: {ip_set['Id']}, Name: {ip_set['Name']}, ARN: {ip_set['ARN']}")

    except Exception as e:
        print(f"Errore durante l'elenco degli IP set: {e}")

if __name__ == "__main__":
    # Crea un parser per gli argomenti da riga di comando
    parser = argparse.ArgumentParser(description='Lista gli IP Set di AWS WAF in base allo scope fornito.')
    
    # Aggiunge un argomento allo script
    parser.add_argument('scope', type=str, choices=['REGIONAL', 'CLOUDFRONT'],
                        help='Lo scope degli IP Set da elencare: "REGIONAL" per risorse regionali, "CLOUDFRONT" per risorse associate a CloudFront.')
    
    # Esegue il parsing degli argomenti
    args = parser.parse_args()

    # Chiama la funzione list_waf_ip_sets con lo scope fornito
    list_waf_ip_sets(args.scope)