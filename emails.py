import smtplib

EMAIL_LOG = "data/email_logins.txt"

def email_logins():

    with open(EMAIL_LOG, "r") as f:
        logins = [line.strip() for line in f]

    return logins

def send_email(sent_from, sent_to, subject, body, password):
    """Function send emails

    Args:
        sent_from (string): Sender email address
        sent_to (string): Target email address
        subject (string): Email subject
        body (string): Email body
        password (string): Password needed to send mail
    """
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """% (sent_from, sent_to, subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(sent_from, password)
        server.sendmail(sent_from, sent_to, message)
        server.close()
    except:
        print("Send error!!!")

def files_downloaded():

    subject = "Files updated"
    body = "The files have been downloaded and updated"
    
    send_email(email_logins()[0], email_logins()[1], subject, body, email_logins()[2])

def download_error():

    subject = "Download Error"
    body = "File download failed"

    send_email(email_logins()[0], email_logins()[1], subject, body, email_logins()[2])