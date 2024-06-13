# balocchini/sts/__init__.py

from .operation import STSOperation

def load_arguments(parser):
    """Carica gli argomenti specifici per le operazioni STS."""
    parser.add_argument('--sts-role-arn', type=str, help='ARN del ruolo da assumere')
    parser.add_argument('--sts-role-session-name', type=str, help='Nome della sessione per il ruolo da assumere')
    parser.add_argument('--sts-target-profile', type=str, help='Nome del profilo target da aggiornare')