import re
import os
import string
import unicodedata
import tweepy as tp
from flask import request, session
from dotenv import load_dotenv

load_dotenv()
CONSUMER_API_KEY = os.environ.get("CONSUMER_API_KEY")
CONSUMER_SECRET_API_KEY = os.environ.get("CONSUMER_SECRET_API_KEY")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
CALLBACK_URL = "http://127.0.0.1:8000/result"
# CALLBACK_URL="https://tsubuyaki-syoten.herokuapp.com/result"


"""
 検索したい単語と取ってきたいTweet数(デフォルトは10)を引数に渡すと，
 検索したい単語を含んだtweetをリストにして返す
"""

def removeSymbol(soup):
    soup = unicodedata.normalize("NFKC", soup)
    exclusion = "〔〕「」『』【】、。・" + "\n" + "\r" + "\u3000"
    soup = soup.translate(str.maketrans("", "", string.punctuation  + exclusion))
    return soup


def getTweetsFromSearchWords(search_word, count=10):
    # CONSUMER_API_KEY = "SOciKVMCVQU4ZqucCpLsf5MvS"
    # CONSUMER_SECRET_API_KEY = "7vcZ4O3zTQ2yulxxLPhICCaOydWGabSEcsTja10viFCrJLHzhz"
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


def getMyFavorites(count=10):
    # CONSUMER_API_KEY = "SOciKVMCVQU4ZqucCpLsf5MvS"
    # CONSUMER_SECRET_API_KEY = "7vcZ4O3zTQ2yulxxLPhICCaOydWGabSEcsTja10viFCrJLHzhz"
    auth = tp.OAuthHandler(CONSUMER_API_KEY, CONSUMER_SECRET_API_KEY)
    api = tp.API(auth)
    url_pattern = re.compile("https://")
    fav_tweets = api.favorites('@unacceptablee2', count)
    results = []
    for tweet in fav_tweets:
        if url_pattern.search(tweet.text):
            continue
        results.append(tweet.text)
    return results


def getFavorites(user_id, count):
    verifier = request.args.get('oauth_verifier')
    auth = tp.OAuthHandler(CONSUMER_API_KEY, CONSUMER_SECRET_API_KEY, CALLBACK_URL)
    token = session['request_token']
    session.pop('request_token', None)
    auth.request_token = token

    try:
        auth.get_access_token(verifier)
    except tp.TweepError as e:
        print("error in getFavorites:", vars(e))

    api = tp.API(auth)
    user_id = api.me().screen_name
    fav_tweets = api.favorites(user_id, count)
    url_pattern = re.compile("https://")
    text_only_tweets = []
    for tweet in fav_tweets:
        if not(url_pattern.search(tweet.text)):
            text_only_tweets.append(tweet)

    fav_tweet_texts = [removeSymbol(t) for t in text_only_tweets]
    return fav_tweet_texts
