from .common import S3Common
from .delete import S3Delete
from .download import S3Download


def load_arguments(parser):
    """Carica gli argomenti specifici per le operazioni S3."""
    parser.add_argument('--s3-bucket', type=str, help='Nome del bucket S3 da gestire')
    parser.add_argument('--s3-directory', type=str, help='Directory di destinazione per il download')