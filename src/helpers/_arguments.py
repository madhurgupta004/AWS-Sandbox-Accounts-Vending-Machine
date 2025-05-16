from typing import List
from argparse import ArgumentParser

_parser = ArgumentParser()

_parser.add_argument(
    '--access-key',
    type=str,
    required=True,
    help='Access key of the user'
)

_parser.add_argument(
    '--secret-access-key',
    type=str,
    required=True,
    help='Secret access key of the user'
)

_args = _parser.parse_args()

access_key: str = _args.access_key
secret_access_key: str = _args.secret_access_key