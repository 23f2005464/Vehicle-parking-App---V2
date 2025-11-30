import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SMTP_SERVER="localhost"
SMTP_PORT=1025
SENDER_EMAIL='papa@example.com'

def send_mail(to,subject,content):
    mess=MIMEMultipart()
    mess['To']=to
    mess['Subject']=subject
    mess['From']=SENDER_EMAIL
    mess.attach(MIMEText(content,'html'))
    with smtplib.SMTP(host=SMTP_SERVER,port=SMTP_PORT) as client:
        client.send_message(mess)
        client.quit()
        
  