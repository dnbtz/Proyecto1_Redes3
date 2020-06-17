import smtplib
import sys
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import time


pngpath = '/home/daniel/PycharmProjects/Proyecto1/Tarea2_3/IMG/'

def sendEmail(subject, imag):
    time.sleep(5)

    msg = MIMEMultipart()
 
    msg['Subject'] = subject
 
 
    msg['From'] = 'dummycuentaredes3@gmail.com'
    msg['To'] = 'dummycuentaredes3@gmail.com'
    password = "Secreto123@"

    fp = open(pngpath+imag, 'rb')

    msg.attach(MIMEImage(fp.read()))
 
    
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
 
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
 
 
    # send the message via the server.
    s.sendmail(msg['From'], msg['To'], msg.as_string())
 
    s.quit()
 
    sys.exit("correo correctamente enviado a %s:" % (msg['To']))

