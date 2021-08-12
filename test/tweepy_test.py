import os
import tweepy as tp
from dotenv import load_dotenv

load_dotenv()

CONSUMER_API_KEY = os.environ.get("CONSUMER_API_KEY")
CONSUMER_SECRET_API_KEY = os.environ.get("CONSUMER_SECRET_API_KEY")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

auth = tp.OAuthHandler(CONSUMER_API_KEY, CONSUMER_SECRET_API_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tp.API(auth)

fav_tweets = api.favorites()
for tweet in fav_tweets:
    print("-------------------")
    print(tweet.text)
