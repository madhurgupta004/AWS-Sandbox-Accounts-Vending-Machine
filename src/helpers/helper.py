import random
import string

import smtplib
from email.mime.text import MIMEText



smtp_user = "guptamadhur63@gmail.com"
smtp_pass = ""
smtp_server = "smtp.gmail.com"
smtp_port = 587


def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%&*"
    return ''.join(random.choice(chars) for _ in range(length))

def send_email(user_name, password, user_email, account_id):
    console_url =f"https://{account_id}.signin.aws.amazon.com/console"
    email_body = f"""
    Hi {user_name},

    Your AWS IAM user account has been created.

    Username: {user_name}
    Initial Password: {password}
    Console Login URL: {console_url}

    Please log in and reset your password.

    Regards,
    Admin Team
    """

    msg = MIMEText(email_body)
    msg["Subject"] = "Your AWS IAM Account Credentials"
    msg["From"] = smtp_user
    msg["To"] = user_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, user_email, msg.as_string())