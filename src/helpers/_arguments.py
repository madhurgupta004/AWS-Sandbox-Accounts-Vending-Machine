from argparse import ArgumentParser

_parser = ArgumentParser()

_parser.add_argument(
    '--initial-account-data-key',
    type=str,
    required=True,
    help='S3 key for the initial account data'
)

_args = _parser.parse_args()

initial_account_data_s3_key: str = _args.initial_account_data_key