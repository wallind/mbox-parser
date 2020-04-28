import sys
import re
import csv
import mailbox
import numpy
from numpy import savetxt


OUTPUT_FILE_PATH = "./bodyData.csv"
PATH_TO_MBOX_FILE = "C:/Users/Horatio/Desktop/All mail Including Spam and Trash.mbox"

mailboxObj = mailbox.mbox(PATH_TO_MBOX_FILE)

observedCharsets = set()
multipartEmails = 0
emailBodyData = []
emailsProcessed = 0
errorCount = 0
iterCount = 15

for email in mailboxObj:
	if email.is_multipart(): multipartEmails += 1
 
	while email.is_multipart():
		email = email.get_payload()[0]
	 
	text = email.get_payload(decode=True)
 
	if (len(email.get_charsets()) == 0): print('one')
 
	for charset in email.get_charsets():
		if (charset != None):
			observedCharsets.add(charset)
			try:
				text = text.decode(charset)
				text = text.replace('\n', '')
				text = text.replace('\r', '')
				text = text.replace(',', '')
				text = re.sub(r'<style[^>]*>([^<]+)<\/style>', '', text)
				text = re.sub(r'<head[^>]*>([^<]+)<\/head>', '', text)
				text = re.sub(r'<[^>]*>', '', text)
    
				emailBodyData.append(text)
			except:
				errorCount += 1
				print(f"errored trying to decode payload using: {charset} from result of get_charsets: {email.get_charsets()}")
			
	emailsProcessed += 1
	


print(f"Observed charsets: {observedCharsets}")
print(f"Emails Processed: {emailsProcessed}")
print(f"Harvested Data length: {len(emailBodyData)}")
print(f"Multipart Emails: {multipartEmails}")
print(f"Error Count: {errorCount}")
savetxt(OUTPUT_FILE_PATH, emailBodyData, delimiter=',', fmt='%s', encoding='utf-8-sig')


with open(OUTPUT_FILE_PATH, encoding="utf-8-sig") as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
 
	rows = list(csv_reader)
	rowCount = len(rows)
	print(f"Data samples in saved CSV file: {rowCount}")