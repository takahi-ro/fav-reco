import re
import os
import tweepy as tp
from flask import request, session
from dotenv import load_dotenv

load_dotenv()
CONSUMER_API_KEY = os.environ.get("CONSUMER_API_KEY")
CONSUMER_SECRET_API_KEY = os.environ.get("CONSUMER_SECRET_API_KEY")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
CALLBACK_URL = "http://127.0.0.1:8000/favorites"
# CALLBACK_URL="https://young-dawn-36523.herokuapp.com/favorites"
"""
 検索したい単語と取ってきたいTweet数(デフォルトは10)を引数に渡すと，
 検索したい単語を含んだtweetをリストにして返す
"""
def getTweetsFromSearchWords(search_word, count=10):
    CONSUMER_API_KEY = "SOciKVMCVQU4ZqucCpLsf5MvS"
    CONSUMER_SECRET_API_KEY = "7vcZ4O3zTQ2yulxxLPhICCaOydWGabSEcsTja10viFCrJLHzhz"
    auth = tp.OAuthHandler(CONSUMER_API_KEY, CONSUMER_SECRET_API_KEY)
    api = tp.API(auth)
    url_pattern = re.compile("https://")
    tweets = tp.Cursor(api.search, q=search_word, lang="ja").items(count)
    results = []
    for tweet in tweets:
        if url_pattern.search(tweet.text):
            continue
        results.append(tweet.text)
    return results


def getFavorites():
    verifier = request.args.get('oauth_verifier')
    auth = tp.OAuthHandler(CONSUMER_API_KEY, CONSUMER_SECRET_API_KEY, CALLBACK_URL)
    token = session['request_token']
    session.pop('request_token', None)
    auth.request_token = token

    try:
        auth.get_access_token(verifier)
    except tp.TweepError as e:
        print(vars(e))

    api = tp.API(auth)
    user_id = api.me().screen_name
    fav_tweets = api.favorites(user_id, count=10)
    url_pattern = re.compile("https://")
    text_only_tweets = []
    for tweet in fav_tweets:
        if not(url_pattern.search(tweet.text)):
            text_only_tweets.append(tweet)
    return text_only_tweets
