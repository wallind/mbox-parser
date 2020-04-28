import sys

import mailbox

mailboxObj = mailbox.mbox("C:/Users/Horatio/Desktop/All mail Including Spam and Trash.mbox")


observedCharsets = set()
maxMultipartDepth = 0
multipartEmails = 0
emailBodyData = []
emailsProcessed = 0
errorCount = 0
iterCount = 15

for email in mailboxObj:
	if email.is_multipart(): multipartEmails += 1
	multipartDepth = 0	
 
	while email.is_multipart():
		multipartDepth += 1
		email = email.get_payload()[0]
		if multipartDepth > maxMultipartDepth: maxMultipartDepth = multipartDepth
	 
	text = email.get_payload(decode=True)
 
	for charset in email.get_charsets():
		if (charset != None):
			observedCharsets.add(charset)
			try:
				text = text.decode(charset)
			except:
				errorCount += 1
				print(f"errored trying to use {charset} from {email.get_charsets()}")

	emailBodyData.append(text)		
	emailsProcessed += 1
  


print(f"Max multipart depth: {maxMultipartDepth}")
print(f"Observed charsets: {observedCharsets}")
print(f"Emails Processed: {emailsProcessed}")
print(f"Harvested Data length: {len(emailBodyData)}")
print(f"Multipart Emails: {multipartEmails}")
print(f"Error Count: {errorCount}")