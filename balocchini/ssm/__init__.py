from .ec2session import EC2Session

def load_arguments(parser):
    """Carica gli argomenti specifici per le operazioni SSM."""
    parser.add_argument('--ssm-i', type=str, help='ID dell\'istanza EC2 per la sessione SSM')