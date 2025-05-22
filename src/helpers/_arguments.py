from argparse import ArgumentParser

_parser = ArgumentParser()

# _parser.add_argument(
#     '--access-key',
#     type=str,
#     required=True,
#     help='Access key of the user'
# )

# _parser.add_argument(
#     '--secret-access-key',
#     type=str,
#     required=True,
#     help='Secret access key of the user'
# )

_parser.add_argument(
    '--initial-account-data-key',
    type=str,
    required=True,
    help='S3 key for the initial account data'
)

_args = _parser.parse_args()

# access_key: str = _args.access_key
# secret_access_key: str = _args.secret_access_key
initial_account_data_key: str = _args.initial_account_data_key