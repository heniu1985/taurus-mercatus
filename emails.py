import smtplib

def send_email(sent_from, sent_to, subject, body, password):
    """Function send emails

    Args:
        sent_from (string): Sender email address
        sent_to (string): Target email address
        subject (string): Email subject
        body (string): Email body
        password (string): Password needed to send mail
    """
    email = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, sent_to, subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(sent_from, password)
        server.sendmail(sent_from, sent_to, email)
        server.close()
    except:
        print("Send error!!!")

# filename = "data/email_log.txt"

# with open(filename, "r") as f:
#     email_list = [line.strip() for line in f]

# sent_from = email_list[0]
# sent_to = email_list[1]
# password = email_list[2]
# subject = "Test"
# body = """
# Test
# test test test
# """

# send_email(sent_from, sent_to, subject, body, password)