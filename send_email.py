import os
from dotenv import load_dotenv
import smtplib, ssl

load_dotenv()


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    user_mail = "jay.ravalani746@gmail.com"
    password = os.getenv("PASSWORD")

    receiver_mail = "jay.ravalani746@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(user_mail, password)
        server.sendmail(user_mail, receiver_mail, message)
