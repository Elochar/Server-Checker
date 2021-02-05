import smtplib
from email.message import EmailMessage

# Add your email and app password for this to work.

def email_alert(subject, body, to):

    msg = EmailMessage()
    msg.set_content(body)

    # UPDATE THESE LINES TO YOUR INFO
    gmail_user = 'chpopo12@gmail.com'
    gmail_password = 'Your_Password'
    msg['Subject'] = subject
    msg['From'] = "chpopo12@gmail.com"
    msg['To'] = to


    # Send the message via our own SMTP server.
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login(gmail_user, gmail_password)
    s.send_message(msg)
    s.quit()

if __name__ == '__main__':
    email_alert("Test","https://www.youtube.com/","8025050264@vtext.com")