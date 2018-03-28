import smtplib

message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
MIME-Version: 1.0
Content-type: text/html
Subject: SMTP HTML e-mail test

This is an e-mail message to be sent in HTML format

<b>This is HTML message.</b>
<h1>This is headline.</h1>
"""

try:
   smtpObj = smtplib.SMTP(host='localhost',port=1025)
   smtpObj.sendmail("test", "aditya.farizki1@gmail.com", message)         
   print "Successfully sent email"
except Exception as e:
   print e