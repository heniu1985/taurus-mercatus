import smtplib
import getpass

mail_user = getpass.getpass("Login: ")
mail_password = getpass.getpass("Password: ")

sent_from = mail_user

sent_to = getpass.getpass("Sent to: ")

subject = "Taurus Mercatus"

body = "This is mail body"

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, sent_to, subject, body)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(mail_user, mail_password)
    server.sendmail(sent_from, sent_to, email_text)
    server.close()
    
    print("OK")
except:
    print("Something wrong!!!")