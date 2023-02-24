from email.mime.text import MIMEText
import os
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
import re
from src.services.gmail_service.templates import templates

def _send_email(email_receiver, subject, body):
    load_dotenv()
    email_sender = os.environ['GMAIL_ADDRESS']
    email_password = os.environ['GMAIL_APP_PASSWORD']

    em = None
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

def _validate_title(s):
    if len(s) > 200:
        raise Exception("name is too long")

def _validate_email(s):
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.match(pat,s):
        raise Exception("Invalid Email")

def _validate_email_message_information(email, name1, name2):
    try:
        _validate_email(email)
        _validate_title(name1)
        _validate_title(name2)
        return False
    except Exception as e:
        print("email validation failed: " + str(e))
        return True

# sends notification to tutor about new request
def send_tutorship_request_email(tutor_email, student_name, course_name):
    # validate input
    if _validate_email_message_information(tutor_email, student_name, course_name):
        return
    # send email
    subject = templates["TUTORSHIP_REQUEST_SUBJECT"]
    body = MIMEText(templates["TUTORSHIP_REQUEST_BODY"].format(student_name=student_name, course_name=course_name), 'html')
    _send_email(tutor_email, subject, body)

# sends notification to student about request accept
def send_tutorship_accept_email(tutor_email, tutor_name, course_name):
    # validate input
    if _validate_email_message_information(tutor_email, tutor_name, course_name):
        return
    # send email
    subject = templates["TUTORSHIP_ACCEPT_SUBJECT"]
    body = MIMEText(templates["TUTORSHIP_ACCEPT_BODY"].format(tutor_name=tutor_name, course_name=course_name), 'html')
    _send_email(tutor_email, subject, body)

# sends notification to student about request deny
def send_tutorship_deny_email(tutor_email, tutor_name, course_name):
    # validate input
    if _validate_email_message_information(tutor_email, tutor_name, course_name):
        return
    # send email
    subject = templates["TUTORSHIP_DENY_SUBJECT"]
    body = MIMEText(templates["TUTORSHIP_DENY_BODY"].format(tutor_name=tutor_name, course_name=course_name), 'html')
    _send_email(tutor_email, subject, body)

# sends notification to tutor about tutor course accept (only if they have never tutored before)
def send_tutor_course_first_accept_email(tutor_email, tutor_name, course_name):
    # validate input
    if _validate_email_message_information(tutor_email, tutor_name, course_name):
        return
    # send email
    subject = templates["TUTOR_COURSE_ACCEPT_FIRST_SUBJECT"]
    body = MIMEText(templates["TUTOR_COURSE_ACCEPT_FIRST_BODY"].format(tutor_name=tutor_name, course_name=course_name), 'html')
    _send_email(tutor_email, subject, body)

# sends notification to tutor about tutor course accept
def send_tutor_course_accept_email(tutor_email, course_name):
    # validate input
    if _validate_email_message_information(tutor_email, course_name, course_name):
        return
    # send email
    subject = templates["TUTOR_COURSE_ACCEPT_SUBJECT"]
    body = MIMEText(templates["TUTOR_COURSE_ACCEPT_BODY"].format(course_name=course_name), 'html')
    _send_email(tutor_email, subject, body)

# send notification to tutor about tutor course denial
def send_tutor_course_deny_email(tutor_email, course_name):
    # validate input
    if _validate_email_message_information(tutor_email, course_name, course_name):
        return
    # send email
    subject = templates["TUTOR_COURSE_DENY_SUBJECT"]
    body = MIMEText(templates["TUTOR_COURSE_DENY_BODY"].format(course_name=course_name), 'html')
    _send_email(tutor_email, subject, body)
