
import tweepy
import json
import authconfig
import pandas as pd

# tweepy authentication

auth = tweepy.OAuthHandler(authconfig.consumer_key, authconfig.consumer_secret)
auth.set_access_token(authconfig.access_key, authconfig.access_secret)
api = tweepy.API(auth)

# design two dictionaries to hold woeid of places (countries and cities)
# so that we'll not have to manually search for a country's woeid

city_names_woeid = {}
country_names_woeid = {}
for trends in api.trends_available():
    if trends['parentid'] == 1:
        country_names_woeid[trends['country']] = trends['woeid']      # just get country data to exclude cities where
                                                                      # parent id is the same as worldwide id
    elif trends['parentid'] != 1:
        city_names_woeid[trends['name']] = trends['parentid']
        country_names_woeid[trends['country']] = trends['woeid']
    else:
        pass

# combine the two dictionaries
city_country_names_woeid = {**city_names_woeid, **country_names_woeid}

# list of topics
topics = []

# the country in question
country = 'Kenya'

try:
    city_country_trends = api.trends_place(city_country_names_woeid[country])

    trends = json.loads(json.dumps(city_country_trends, indent=1))

    for trend in trends[0]["trends"][:10]:      # top ten trends
        topics.append((trend["name"]))
        #print(trend["name"])#.strip("#"))
        #print(trend["name"])

except KeyError as e:
    print(f"There is no trending topic information for the currently selected city/country: {e}")

# save the topics as csv file(pandas series)
topics = pd.DataFrame({'topics': topics})
topics.to_csv("csv files/topics.csv", index=False)