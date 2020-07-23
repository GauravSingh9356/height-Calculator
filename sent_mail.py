from email.mime.text import MIMEText
import smtplib

def sent_email(email, height, avg_height, count):
    from_email = process.env.email
    from_password=process.env.password
    to_email=email
    subject='Height data'
    message='Hey there, your height is <strong>%s</strong>.<br/> Average height of all is <strong>%s</strong>. <br/><strong>%s</strong> no of people are recorded.<br/>Thanks!' % (height, avg_height, count)
    msg=MIMEText(message, 'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email
    
    gmail=smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)