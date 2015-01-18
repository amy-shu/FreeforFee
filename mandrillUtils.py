import mandrill


def sendEmail(messageText, receivingEmail, receivingName='Recipient'):
        mandrill_client = mandrill.Mandrill('PsG4nAwAdNKbM8G8MymE1Q')
        message = {
        'auto_html': None,
        'auto_text': None,
        'from_email': 'postmates@pavleen.me',
        'from_name': 'FreeForFee',
        'global_merge_vars': [{'content': 'merge1 content', 'name': 'merge1'}],
        'important': False,
        'inline_css': None,
        'merge': True,
        'merge_language': 'mailchimp',
        'merge_vars': [{'rcpt': 'recipient.email@example.com',
        'vars': [{'content': 'merge2 content', 'name': 'merge2'}]}],
        'subject': 'CraigsList Request',
        'text': messageText,
        'to': [{'email': receivingEmail,
                'name': receivingName,
                'type': 'to'}]
        }
        mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')

sendEmail('yo whatup','pav920@gmail.com')
