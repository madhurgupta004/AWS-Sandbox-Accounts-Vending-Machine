from argparse import ArgumentParser

_parser = ArgumentParser()

_parser.add_argument(
    '--final-account-data-bucket',
    type=str,
    required=True,
    help='S3 key for the initial account data'
)

_parser.add_argument(
    '--ses-verified-source-email',
    type=str,
    required=True,
    help='SES verified source email address for sending welcome emails'
)

_parser.add_argument(
    '--root-ou-id',
    type=str,
    required=True,
    help='Id of root organizational unit'
)

_parser.add_argument(
    '--sandbox-ou-id',
    type=str,
    required=True,
    help='Id of sandbox organizational unit'
)

_parser.add_argument(
    '--ses-identities-region',
    type=str,
    required=True,
    help='AWS region where SES identities are verified'
)


_args = _parser.parse_args()

final_account_data_bucket: str = _args.final_account_data_bucket
source_email: str = _args.ses_verified_source_email
root_ou: str = _args.root_ou_id
sandbox_ou: str = _args.sandbox_ou_id
ses_region: str = _args.ses_identities_region