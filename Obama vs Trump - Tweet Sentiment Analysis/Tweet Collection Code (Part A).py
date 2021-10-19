# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 13:31:42 2018

@author: Kofi Buahin
"""

#Part A. Tweet Data Collection

import json
import sys
twit_cred = {
    "CONSUMER_KEY" : "cZihRCXqdHxcOie0OPj0eL6bc",
    "CONSUMER_SECRET" : "8jbYaMFAwSeysVhWM9MaN3BCHHt4dINYpey0l1CSivTGcEW5mg",
    "ACCESS_TOKEN" :  "934692384-J2bPQfEYbYwgYlxh4A0uJzYWiuWqwtXGQ0zcqSXb",
    "ACCESS_TOKEN_SECRET" : "cVIONdXwIDEc0V8X39f1ttFYTkkKooAu49okdw27CGSWE"
}
with open('Kofi_twitter_credentials.json', 'w') as f:
    json.dump(twit_cred, f)

with open('Kofi_twitter_credentials.json', 'r') as f:
    credentials = json.load(f)

KOFIC_KEY = credentials['CONSUMER_KEY']
KOFIC_SECRET = credentials['CONSUMER_SECRET']
KOFIA_TOKEN = credentials['ACCESS_TOKEN']
KOFIA_TOKENSECRET = credentials['ACCESS_TOKEN_SECRET']

from twython import TwythonStreamer
tweets = []

# Github Code: https://github.com/ryanmcgrath/twython/blob/master/twython/streaming/api.py
class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'lang' in data and data['lang'] == 'en':
            tweets.append(data)
            print('received tweet #', len(tweets), data['text'][:100])
        if len(tweets) >= 10000:
            self.store_json()
            self.disconnect()
    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()
    def store_json(self):
        with open('tweet_stream_{}_{}.json'.format(keyword, len(tweets)), 'w') as f:
            json.dump(tweets, f, indent=4)
            
if __name__ == '__main__':
    with open('Kofi_twitter_credentials.json', 'r') as f:
        credentials = json.load(f)
    KOFIC_KEY = credentials['CONSUMER_KEY']
    KOFIC_SECRET = credentials['CONSUMER_SECRET']
    KOFIA_TOKEN = credentials['ACCESS_TOKEN']
    KOFIA_TOKENSECRET = credentials['ACCESS_TOKEN_SECRET']
    stream = MyStreamer(KOFIC_KEY, KOFIC_SECRET, KOFIA_TOKEN, KOFIA_TOKENSECRET)
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
    else:
        keyword = 'Obama'

    # Github Code: https://github.com/ryanmcgrath/twython/blob/master/twython/streaming/api.py
    # Accepted parameters: https://developer.twitter.com/en/docs/tweets/filter-realtime/api-reference/post-statuses-filter
    stream.statuses.filter(track=keyword)
   


