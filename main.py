import base64
import imaplib
from operator import attrgetter, itemgetter
from app import llm_complete
from draft import create_reply_draft
from inbox import get_inbox, login
from response import classify_email_needs_response

def authenticate_imap(email, oauth2_string):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        mail.authenticate('XOAUTH2', lambda x: oauth2_string)
        print("Authentication successful!")
    except imaplib.IMAP4.error as e:
        print(f"Authentication failed: {e}")
        return None

    return mail


def main():

    email = "" #PUT EMAIL HERE
    access_token = ''#PUT ACCESS TOKEN HERE

    auth_string = 'user=%s\1auth=Bearer %s\1\1' % (email, access_token)

    mail = authenticate_imap(email, auth_string)

    if not mail:
           print('failed')
           return 

    mail.select('inbox')
    


    all_emails = get_inbox(mail)
   
    if all_emails:
        print(all_emails[0])
        email_to_reply = sorted(all_emails, key=itemgetter('uid'), reverse=True)[1]
        #replys to first email rn, u can implement for loop to go through all unreads
        print(email_to_reply)
        uid = email_to_reply['uid']

        response_needed = classify_email_needs_response(email_to_reply)
        print(response_needed)
        if response_needed.get('needs_response'):
            reply_body_text = llm_complete(email_to_reply)['choices'][0].get('message', '').get('content')
            print(reply_body_text)
            create_reply_draft(mail, uid, reply_body_text)
        else:
            print('No response needed for this email.')
    else:
        print('No emails found.')



if __name__ == "__main__":
    main()