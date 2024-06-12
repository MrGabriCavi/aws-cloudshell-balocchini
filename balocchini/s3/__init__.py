# balocchini/s3/__init__.py

from .common import S3Common
from .delete import S3Delete
from .download import S3Download
from .operation import S3Operation

def load_arguments(parser):
    """Carica gli argomenti specifici per le operazioni S3."""
    parser.add_argument('--s3-bucket', type=str, help='Nome del bucket S3 da gestire')
    parser.add_argument('--s3-directory', type=str, help='Directory di destinazione per il download')
    parser.add_argument('--s3-md-include', type=str, nargs='*', help='Elenco di bucket da includere per il download multiplo')
    parser.add_argument('--s3-md-exclude', type=str, nargs='*', help='Elenco di bucket da escludere per il download multiplo')