import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

def load_smtp_config(file_path):
    """ Load SMTP configuration from JSON file """
    with open(file_path) as f:
        smtp_config = json.load(f)
    return smtp_config

def send_email(recipient, message):
    """ Send permissions email """
    smtp_config = load_smtp_config('email_config.json')
    smtp_server = smtp_config['smtp_server']
    port = smtp_config['port']
    sender_email =  base64.b64decode(smtp_config['sender_email']).decode('utf-8')
    password = base64.b64decode(smtp_config['password']).decode('utf-8') 

    subject = 'File Permissions'

    message_body = MIMEMultipart()
    message_body['From'] = sender_email
    message_body['To'] = recipient
    message_body['Subject'] = subject
    message_body.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', port) as smtp_server:
            smtp_server.login(sender_email, password)
            smtp_server.send_message(message_body)
    except Exception as e:
        print("Error sending email:", e)

# Load SMTP configuration from JSON file
smtp_config = load_smtp_config('email_config.json')
