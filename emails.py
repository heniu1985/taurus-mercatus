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
        print("Email sent!!!")
    except:
        print("Send error!!!")

def files_downloaded():
    """Function send email after download the files
    """
    subject = "Files updated"
    body = "The files have been downloaded and updated"
    
    send_email(email_logins()[0], email_logins()[1], subject, body, email_logins()[2])

def download_error():
    """Function sedn email if send error occured
    """
    subject = "Download Error"
    body = "File download failed"

    send_email(email_logins()[0], email_logins()[1], subject, body, email_logins()[2])

def buy_signals(signals_dict):
    """Function send email with buy signal

    Args:
        signals_dict (dict): dictionary with buy signals
    """
    subject = "Buy signals"
    body = "Buy signal for the following stocks:\n"

    keys = []
    for key in signals_dict:
        keys.append(key)
    
    for key in keys:
        body += " " + key + "\n"

    send_email(email_logins()[0], email_logins()[1], subject, body, email_logins()[2])

def sell_signals(signals_dict):
    """Function send email with sell signal

    Args:
        signals_dict (dict): dictionary with sell signals
    """
    subject = "Sell signals"
    body = "Sell signal for the following stocks:\n"

    keys = []
    for key in signals_dict:
        keys.append(key)
    
    for key in keys:
        body += " " + key + "\n"

    send_email(email_logins()[0], email_logins()[1], subject, body, email_logins()[2])

def close_long_signals(signals_dict):
    """Function send email with close long position signals

    Args:
        signals_dict (dict): dictionary with close long position signals
    """
    subject = "Close long signals"
    body = "Close long position signal for the following stocks:\n"

    keys = []
    for key in signals_dict:
        keys.append(key)
    
    for key in keys:
        body += " " + key + "\n"

    send_email(email_logins()[0], email_logins()[1], subject, body, email_logins()[2])

def close_short_signal(signals_dict):
    """Function send email with close short posiotion signals

    Args:
        signals_dict (dict): dictionary with close short position signals
    """
    subject = "Close short signals"
    body = "Close short position signal for the following stocks:\n"

    keys = []
    for key in signals_dict:
        keys.append(key)
    
    for key in keys:
        body += " " + key + "\n"

    send_email(email_logins()[0], email_logins()[1], subject, body, email_logins()[2])

def no_signals(signal):
    """Function to send email when no signals occured

    Args:
        signal (string): string with signal, for example "BUY", "SELL", "CLOSE LONG", "CLOSE"
    """
    subject = "No signals"
    body = "There were no " + signal + " signal."

    send_email(email_logins()[0], email_logins()[1], subject, body, email_logins()[2])