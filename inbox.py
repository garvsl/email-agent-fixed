
import imaplib
import email
from datetime import datetime, timedelta
import chardet
from bs4 import BeautifulSoup

def login(email_address, password):
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993

    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(email_address, password)
    return mail

def safe_decode(byte_data):
    detected = chardet.detect(byte_data)
    encoding = detected['encoding']

    try:
        return byte_data.decode(encoding) if encoding else byte_data.decode()
    except (UnicodeDecodeError, TypeError):
        return byte_data.decode('utf-8', errors='ignore')

def clean_body(html_body):
    soup = BeautifulSoup(html_body, "html.parser")
    text = soup.get_text()
    return text.strip()
def get_inbox(mail):
    one_month_ago = (datetime.now() - timedelta(days=30)).strftime("%d-%b-%Y")

    _, search_data = mail.uid('search', None, f'SINCE {one_month_ago} UNSEEN')
    my_messages = []

    for uid in search_data[0].split():
        email_data = {}
        result, data = mail.uid('fetch', uid, '(BODY.PEEK[])')
        if result != 'OK':
            print(f"Error fetching email UID {uid.decode('utf-8')}")
            continue
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)

        email_data['uid'] = uid.decode('utf-8')

        for header in ['subject', 'To', 'From', 'Date']:
            email_data[header] = email_message.get(header, '')
        body = None
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition'))
                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                    body = part.get_payload(decode=True)
                    break
        else:
            body = email_message.get_payload(decode=True)

        if body:
            bod = safe_decode(body)
            email_data['body'] = clean_body(bod)
        else:
            email_data['body'] = ''

        my_messages.append(email_data)

    return my_messages

