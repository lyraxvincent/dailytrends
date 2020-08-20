import tweepy
import authconfig
import pandas as pd

# tweepy authentication

auth = tweepy.OAuthHandler(authconfig.consumer_key, authconfig.consumer_secret)
auth.set_access_token(authconfig.access_key, authconfig.access_secret)
api = tweepy.API(auth)

def tweets_by_word_search(word):
    # Cursor(pagination)
    result = tweepy.Cursor(api.search, q=word).items(10000) # adjust items accordingly

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
                if tweet.retweeted == False and tweet.lang == 'en':
                    print('Getting tweet: {}'.format(tweet.id))
                    tweet_id.append(tweet.id)
                    tweets.append(tweet.text)
                    created_at.append(tweet.created_at)
                    likes.append(tweet.favorite_count)
                    retweet_count.append(tweet.retweet_count)
                    df.loc[i] = [tweet.id, tweet.text, tweet.created_at, tweet.favorite_count, tweet.retweet_count] # Append data to df

                    # Saving df at every iteration to ensure data is captured regardless of program breakdown
                    df.to_csv(f'{word}.csv', index=False)
        except tweepy.TweepError as e:
            print(f"Please wait...proceeding in a few minutes.\n({e})")
            time.sleep(15 * 60)
            continue

    # printing the tweets
    #print(tweets)
    print(len(tweets))

    # Saving dataframe
    #df.to_csv('covidKE tweets.csv', index=False)

# Calling the function
tweets_by_word_search('JKLive')