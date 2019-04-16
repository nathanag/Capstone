# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:32:01 2019

@author: Nathan
"""

import json
from pprint import pprint
import tweepy #easy_install tweepy, pip install tweepy

# Function to read the key file and load keys in a dictionary
def loadKeys(key_file):
    with open('keys.json') as f:
        key_dict = json.load(f)
    return key_dict['api_key'], key_dict['api_secret'], key_dict['token'], key_dict['token_secret']

# Authenticate using oAuthHandler
KEY_FILE = 'keys.json'
api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(token, token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

tweet_id = tweets[0][1][0].id

tweet = api.get_status(tweet_id)

name = "NYTimes"

import sys
replies=[] 
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)  

for full_tweets in tweepy.Cursor(api.user_timeline,screen_name='NBCNews',timeout=999999).items(10):
  for tweet in tweepy.Cursor(api.search,q='to:NBCNews', since_id=1111301934517051392, result_type='mixed',timeout=999999).items(10):
    if hasattr(tweet, 'in_reply_to_status_id_str'):
      if (tweet.in_reply_to_status_id_str==full_tweets.id_str):
        replies.append(tweet.text)
  print("Tweet :",full_tweets.text.translate(non_bmp_map))
  for elements in replies:
       print("Replies :",elements)
  replies.clear()
  

name="NBCNews"
replies=[] 
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)  
for full_tweets in tweepy.Cursor(api.user_timeline,screen_name=name,timeout=999999).items(10):
  for tweet in tweepy.Cursor(api.search,q='to:'+name,result_type='recent',timeout=999999).items(1000):
    if hasattr(tweet, 'in_reply_to_status_id_str'):
      if (tweet.in_reply_to_status_id_str==full_tweets.id_str):
        replies.append(tweet.text)
  print("Tweet :",full_tweets.text.translate(non_bmp_map))
  for elements in replies:
       print("Replies :",elements)
  replies.clear()