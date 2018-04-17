from writer import TwitterWriter, Tokenization
import tweepy
import config

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)

api = tweepy.API(auth)

TwitterWriter writer = TwitterWriter(5, Tokenization.character)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)