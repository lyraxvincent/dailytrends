from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import authconfig

msg = MIMEMultipart()
toaddr = ['vinsvincybiex@gmail.com']
fromaddr = authconfig.email
#cc = ['mailid_3','mailid_4']
#bcc = ['mailid_5','mailid_6']
subject = 'Final test - Email from Python Code'
body = MIMEText("\n  !! Hello... !!")
msg.attach(body)

msg['From'] = fromaddr
msg['To'] = ', '.join(toaddr)
#msg['Cc'] = ', '.join(cc)
#msg['Bcc'] = ', '.join(bcc)
msg['Subject'] = subject

smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo()
smtpserver.login(authconfig.email, authconfig.emailpass)

for addr in toaddr:
    smtpserver.sendmail(fromaddr, addr, msg.as_string())
    #smtp.sendmail(fromaddr, (toaddr+cc+bcc), msg.as_string())
    print(f"Email sent to {addr}")

smtpserver.quit()