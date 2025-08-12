import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Gmail credentials
    GMAIL_ADDRESS = os.getenv('GMAIL_ADDRESS')
    GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')  # App password

    # File paths
    RESUME_PATH = 'attachments/resume.pdf'
    EMAIL_TEMPLATE_PATH = 'templates/email_template.html'

    # SMTP settings
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
