from writer import TwitterWriter, Tokenization
import tweepy
import config
import itertools
import json
import io

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)

api = tweepy.API(auth)

writer = TwitterWriter(5, Tokenization.character)

user = input('Enter name: ')

l = []
with open('history.jsonl', mode='r', encoding='utf-8') as history:
    for jsonline in history:
        msg_obj = json.loads(jsonline)
        if msg_obj['from']['first_name'] == user:
            text = msg_obj.get('text', None)
            if text is not None and len(text) < 100:
                l.append(text)

large_text = ' '.join(l)
writer.learn_iterable(large_text)
try:
    writer.dump_pickle('markovpickle.txt')
except RecursionError as e:
    print('Error in saving pickle')

for i in range(5):
    out = ''.join(itertools.islice(writer.output(), 200))
    api.update_status(out)
