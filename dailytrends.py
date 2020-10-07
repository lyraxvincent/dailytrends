import schedule
import time

# delete previously used topic files
schedule.every().day.at("06:00").do(python3 get_topics.py)

# collect topics
schedule.every().day.at("07:00").do(python3 get_topics.py)
schedule.every().day.at("09:00").do(python3 get_topics.py)
schedule.every().day.at("11:00").do(python3 get_topics.py)
schedule.every().day.at("13:00").do(python3 get_topics.py)
schedule.every().day.at("15:00").do(python3 get_topics.py)

# collect tweets
schedule.every().day.at("15:30").do(python3 get_tweets_by_topic.py)

# sort csv files
schedule.every().day.at("18:00").do(python3 sort_csv.py)

# clean csv files
schedule.every().day.at("18:05").do(python3 cleanfiles.py)

# send summary news to users
schedule.every().day.at("18:10").do(python3 send_news_to_mail.py)

while True:
    schedule.run_pending()
    time.sleep(1)