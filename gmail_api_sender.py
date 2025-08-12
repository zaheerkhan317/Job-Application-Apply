# gmail_api_sender.py
import base64
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_FILE = 'token.pickle'
CREDENTIALS_FILE = 'credentials.json'

def gmail_login():
    """
    Returns an authorized Gmail service.
    Expects credentials.json and token.pickle to be present.
    If token.pickle not valid and credentials.json present, tries a local auth flow (only works locally).
    """
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # If no valid creds, attempt to refresh or run local flow (local only)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        else:
            if os.path.exists(CREDENTIALS_FILE):
                # This will open a local browser; not suitable for Cloud.
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
                with open(TOKEN_FILE, 'wb') as token:
                    pickle.dump(creds, token)
            else:
                raise FileNotFoundError("credentials.json not found and no valid token available.")

    service = build('gmail', 'v1', credentials=creds)
    return service

def create_message_with_attachment(to, subject, html_body, attachment_path):
    message = MIMEMultipart('mixed')
    message['to'] = to
    message['subject'] = subject

    # HTML body
    body_part = MIMEText(html_body, 'html')
    message.attach(body_part)

    # attachment
    if attachment_path and os.path.exists(attachment_path):
        ctype, encoding = mimetypes.guess_type(attachment_path)
        if ctype is None or encoding:
            ctype = 'application/octet-stream'
        main_type, sub_type = ctype.split('/', 1)

        with open(attachment_path, 'rb') as f:
            part = MIMEBase(main_type, sub_type)
            part.set_payload(f.read())
        encoders.encode_base64(part)

        filename = os.path.basename(attachment_path)
        # use add_header with separate params for better compatibility
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(part)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def send_email(service, to, subject, html_body, attachment_path=None):
    msg = create_message_with_attachment(to, subject, html_body, attachment_path)
    sent = service.users().messages().send(userId='me', body=msg).execute()
    return sent
