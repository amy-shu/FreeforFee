import mandrill

def sendEmail():
	try:
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
		'tags': ['password-resets'],
		'text': 'Example text content',
		'to': [{'email': 'recipient.email@example.com',
			'name': 'Recipient Name',
			'type': 'to'}],
		result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool', send_at='example send_at')
    '''
    [{'_id': 'abc123abc123abc123abc123abc123',
      'email': 'recipient.email@example.com',
      'reject_reason': 'hard-bounce',
      'status': 'sent'}]
    '''

	except mandrill.Error, e:
    	# Mandrill errors are thrown as exceptions
	print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
    	# A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'    
	raise
