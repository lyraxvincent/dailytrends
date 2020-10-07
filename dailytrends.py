import schedule
import time

# scripts
def delprevfiles():
    import delprevfiles

def get_topics():
    import get_topics

def get_tweets_by_topic():
    import get_tweets_by_topic

def sort_csv():
    import sort_csv

def cleanfiles():
    import cleanfiles

def send_news_to_mail():
    import send_news_to_mail

# delete previously used topic files
schedule.every().day.at("06:00").do(delprevfiles)

# collect topics
schedule.every().day.at("07:00").do(get_topics)
schedule.every().day.at("09:00").do(get_topics)
schedule.every().day.at("11:00").do(get_topics)
schedule.every().day.at("13:00").do(get_topics)
schedule.every().day.at("15:00").do(get_topics)

# collect tweets
schedule.every().day.at("15:30").do(get_tweets_by_topic)

# sort csv files
schedule.every().day.at("18:00").do(sort_csv)

# clean csv files
schedule.every().day.at("18:05").do(cleanfiles)

# send summary news to users
schedule.every().day.at("18:10").do(send_news_to_mail)

while True:
    schedule.run_pending()
    time.sleep(1)