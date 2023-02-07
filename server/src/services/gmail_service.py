import os
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv




def _send_email(email_receiver, subject, body):
    load_dotenv()
    email_sender = os.environ['GMAIL_ADDRESS']
    email_password = os.environ['GMAIL_APP_PASSWORD']

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
    except Exception as e:
        print("An error occured while trying to send this email:" + str(e))


def send_tutorship_request_email(tutor_email):
    subject = "Physics Tutoring - New Tutorship Request!"
    body = "Someone has just requested that you tutor them! Check it out on the physics tutoring portal!"
    _send_email(tutor_email, subject, body)