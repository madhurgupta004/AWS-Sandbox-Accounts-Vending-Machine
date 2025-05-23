import string
import secrets


def generate_password():
    """Generate a random 12-character AWS IAM-compliant password."""
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + "!@#$%^&*"
    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*")
    ]
    
    for _ in range(8):
        password.append(secrets.choice(chars))
    
    for i in range(11, 0, -1):
        j = secrets.randbelow(i + 1)
        password[i], password[j] = password[j], password[i]
    
    return ''.join(password)