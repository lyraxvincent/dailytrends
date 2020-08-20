import sys
import tweepy
import json
import authconfig

# Autentication
auth = tweepy.OAuthHandler(authconfig.consumer_key, authconfig.consumer_secret)
auth.set_access_token(authconfig.access_key, authconfig.access_secret)
api = tweepy.API(auth)

result = tweepy.Cursor(api.search, q='JKLive').items(1)
print([tweet.retweeted_status.full_text for tweet in result])