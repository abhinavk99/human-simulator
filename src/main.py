from writer import TwitterWriter, Tokenization
import tweepy
import config
import itertools
import re

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)

api = tweepy.API(auth)

writer = TwitterWriter(50, Tokenization.character)

for tweet in api.home_timeline():
    # Remove all links from the text using regex and newlines
    text = re.sub(r'http\S+', '', tweet.text)
    text = text.replace('\n', '')
    writer.learn_iterable(text)

out_tweet = ''.join(itertools.islice(writer.output(), 200))
api.update_status(out_tweet)
