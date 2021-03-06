import tweepy
import time
#import authconfig
import pandas as pd
import random
import os

# tweepy authentication

#auth = tweepy.OAuthHandler(authconfig.consumer_key, authconfig.consumer_secret)
auth = tweepy.OAuthHandler(os.environ.get('consumer_key'), os.environ.get('consumer_secret'))
#auth.set_access_token(authconfig.access_key, authconfig.access_secret)
auth.set_access_token(os.environ.get('access_key'), os.environ.get('access_secret'))
api = tweepy.API(auth)

def tweets_by_word_search(word):
    # Cursor(pagination)
    result = tweepy.Cursor(api.search, q=word).items(50000) # adjust items accordingly

    tweet_id = []
    tweets = []
    created_at = []
    likes = []
    retweet_count = []
    df = pd.DataFrame(columns=['tweet_id', 'text', 'created_at', 'likes', 'retweet_count'])
    # Time limit error/ exception handling
    while True:
        try:
            for i, tweet in enumerate(result):
                # Filter out retweets and other languages
                if 'RT @' not in tweet.text and 'https:/' not in tweet.text and tweet.lang == 'en':
                    print('Getting tweet: {}'.format(tweet.id))
                    tweet_id.append(tweet.id)
                    tweets.append(tweet.text)
                    created_at.append(tweet.created_at)
                    likes.append(tweet.favorite_count)
                    retweet_count.append(tweet.retweet_count)
                    df.loc[i] = [tweet.id, tweet.text, tweet.created_at, tweet.favorite_count, tweet.retweet_count] # Append data to df

                    # Saving df at every iteration to ensure data is captured regardless of program breakdown
                    df.to_csv(f'csv files/{word}.csv', index=False)
        except tweepy.TweepError as e:
            print(f"\nPlease wait...proceeding in a few minutes.\n({e})\n")
            time.sleep(15 * 60)
            #continue
            break


# Calling the function on every topic in topics.csv
topics = pd.read_csv("csv files/topics.csv")
topics = list(topics.topics)

# pick the most relevant topics
val_topics = []
for topic in topics:
    if topics.count(topic) > 1:     # first pick those with occurrence >1
        val_topics.append(topic)
        topics[:] = [item for item in topics if item != topic]      # remove element from list to avoid adding duplicate value in loop below

# ensure we have 5 topics
while len(val_topics) < 5:
    val_topics.append(random.choice(topics[-5:]))   # pick from the last 5 elements(last collected set)

for topic in val_topics:
    tweets_by_word_search(topic)
