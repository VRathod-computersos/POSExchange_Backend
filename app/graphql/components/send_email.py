import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(receiver_email, subject, body):
    sender_email = "VRathod@computersosinc.com"
    sender_password = "Now82890"

    msg = MIMEMultipart()
    msg["from"] = sender_email
    msg["to"] = receiver_email
    msg["subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, sender_password)
        server.send_message(msg)

send_email("sameeer.deshmukh@gmail.com", "Hii", "hello")
print("Email sent successfully")
