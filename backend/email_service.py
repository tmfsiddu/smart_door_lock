from flask_mail import Mail, Message
from flask import Flask
from config import *

mail = Mail()

def init_mail(app):
    app.config.from_object("config")
    mail.init_app(app)

def send_email(to, subject, body):

    msg = Message(subject,
                  recipients=[to],
                  body=body)

    mail.send(msg)


# NEW FUNCTION FOR DOOR UNLOCK EMAIL
def send_unlock_email(to, token):

    link = f"http://127.0.0.1:5000/unlock/{token}"

    msg = Message(
        subject="Smart Door Lock Verification",
        recipients=[to]
    )

    msg.body = f"""
        OTP verification successful.

        Click the link below to unlock the door:

        {link}
"""

    mail.send(msg)