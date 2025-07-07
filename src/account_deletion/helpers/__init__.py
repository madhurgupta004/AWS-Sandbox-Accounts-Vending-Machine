import os

from ._arguments import account_id

ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

__all__ = [
    'account_id',
    'ACCESS_KEY',
    'SECRET_ACCESS_KEY'
]