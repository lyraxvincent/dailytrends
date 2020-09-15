from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import pandas as pd
import authconfig   # script
import get_topics   # script
import datetime
from summarize import get_summary

# today's date
now = datetime.datetime.now()

# read in the list of sorted topics
topics = pd.read_csv("csv files/sortopics.csv")
topics = [topic for topic in list(topics.topics)]

toaddr = ['vinsvincybiex@gmail.com']
fromaddr = authconfig.email
subject = "Trending topics in {} for {}".format(get_topics.country, now.strftime("%Y-%m-%d"))

msg = MIMEMultipart()
#cc = ['mailid_3','mailid_4']
#bcc = ['mailid_5','mailid_6']
body = ''
for topic in topics:
    df = pd.read_csv(f"csv files/{topic}")
    print(f"Getting summary for topic: [{topic.strip('.csv')}]")
    summary = get_summary(df)
    body += "\n {}\nAbout {}\n===================================\n{}\n".format(topic.split('.csv')[0] \
                                                                                .strip('#').upper(),
                                                                                topic.strip('.csv'), summary)

body = MIMEText(body)
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