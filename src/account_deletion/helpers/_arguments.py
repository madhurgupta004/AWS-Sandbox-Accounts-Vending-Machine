from argparse import ArgumentParser

_parser = ArgumentParser()

_parser.add_argument(
    '--account-id',
    type=str,
    required=True,
    help='S3 key for the initial account data'
)

_args = _parser.parse_args()

account_id: str = _args.account_id