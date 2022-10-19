import smtplib
from email.message import EmailMessage

from _config import PWD, USR


def email(subject: str, body: str):
    msg = EmailMessage()
    msg.set_content(body)

    # Send message to self
    msg["From"] = USR
    msg["To"] = USR
    msg["Subject"] = subject

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(USR, PWD)
    server.send_message(msg)
    server.quit()
