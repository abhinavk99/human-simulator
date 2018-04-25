from markovwriter import TwitterWriter
import config
import itertools
import json
import tweepy

# Login to Twitter
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)

api = tweepy.API(auth)

# Create an empty Level 5 Markov chain
writer = TwitterWriter(5)

# Ask for the name of the user to simulate
user = input('Enter name: ')

l = []
# Go through the message logs
with open('history.jsonl', mode='r', encoding='utf-8') as history:
    for jsonline in history:
        msg_obj = json.loads(jsonline)
        if msg_obj['from']['first_name'] == user:
            text = msg_obj.get('text', None)
            # Add short messages to the list of messages
            if text is not None and len(text) < 100:
                l.append(text)

# Create the Markov chain from the combined text
large_text = ' '.join(l)
writer.learn_iterable(large_text)

# Save the Markov chain for later usage
try:
    writer.dump_pickle('markovpickle.txt')
except RecursionError as e:
    print('Error in saving pickle')

# Make a few tweets using the data
for i in range(5):
    out = ' '.join(itertools.islice(writer.output(), 50))
    api.update_status(out)
