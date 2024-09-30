import email
from email.utils import formatdate, make_msgid
import imaplib
import re
import time

def get_plain_text_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                charset = part.get_content_charset('utf-8')
                return part.get_payload(decode=True).decode(charset, errors='replace')
    else:
        charset = msg.get_content_charset('utf-8')
        return msg.get_payload(decode=True).decode(charset, errors='replace')
    return ''

def create_reply_draft(mail, original_email_uid, reply_body_text):
    result, data = mail.uid('fetch', original_email_uid, '(RFC822)')
    if result != 'OK':
        print(f'Error fetching message UID {original_email_uid}: {result}')
        return

    raw_email = data[0][1]
    original_email = email.message_from_bytes(raw_email)
    original_subject = original_email.get('Subject', '')
    original_from = original_email.get('From', '')
    original_to = original_email.get('To', '')
    original_message_id = original_email.get('Message-ID', '')
    original_date = original_email.get('Date', '')

    if re.match(r'(?i)^\s*Re:\s*', original_subject):
        reply_subject = original_subject
    else:
        reply_subject = 'Re: ' + original_subject

    in_reply_to = original_message_id
    references = original_email.get('References', '')
    if references:
        references += ' ' + original_message_id
    else:
        references = original_message_id

    original_body = get_plain_text_body(original_email)
    quoted_original = '\n'.join(['> ' + line for line in original_body.splitlines()])

    reply_body = f"""{reply_body_text}

On {original_date}, {original_from} wrote:
{quoted_original}
"""

    reply_message = email.message.EmailMessage()
    reply_message['From'] = '' #p UT UR EMAI LHERE 
    reply_message['To'] = original_from
    reply_message['Subject'] = reply_subject
    reply_message['Date'] = formatdate(localtime=True)
    reply_message['Message-ID'] = make_msgid()
    reply_message['In-Reply-To'] = in_reply_to
    reply_message['References'] = references

    reply_message.set_content(reply_body)
    reply_message.set_charset('utf-8')


    encoded_message = reply_message.as_bytes()


    mail.select('"[Gmail]/Drafts"') 
    result = mail.append('"[Gmail]/Drafts"', '', imaplib.Time2Internaldate(time.time()), encoded_message)
    if result[0] != 'OK':
        print('Error saving draft:', result)
    else:
        print('Draft saved successfully.')