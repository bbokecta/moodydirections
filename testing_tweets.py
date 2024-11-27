import tweepy
import json

with open("twitter_keys.json", "r") as twitter_file:
    tokens = json.load(twitter_file)

twitter_file.close()

api_key = tokens['api_key']
api_key_secret = tokens["api_secret"]
access_token = tokens['access_token']
token_secret = tokens['token_secret']
bearer_token = tokens['bearer_token']

client = tweepy.Client(bearer_token=bearer_token)




client.search_all_tweets(query="Billingsgate")