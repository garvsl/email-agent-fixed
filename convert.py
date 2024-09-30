def convert_json(email_json):

    subject = email_json.get('subject', '')
    to = email_json.get('To', '')
    from_ = email_json.get('From', '')
    date = email_json.get('Date', '')
    body = email_json.get('body', '')
    
    plain_email = f"""From: {from_}
    To: {to}
    Subject: {subject}
    Date: {date}

    {body}
    """
    return plain_email
