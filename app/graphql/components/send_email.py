import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from dotenv import load_dotenv

# load_dotenv()
print("Hiii")

def send_email(receiver_email, subject, body):
    sender_email = "Vrathod@computersosinc.com"
    print("Sender Email: ", sender_email)
    sender_password = "Now82890"

    subject = subject
    print(subject)
    msg = MIMEMultipart()
    msg["from"] = sender_email
    msg["to"] = receiver_email
    msg["subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.office365.com", 25) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, sender_password)
        server.send_message(msg)

