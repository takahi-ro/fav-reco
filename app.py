import os
import re
import tweepy as tp
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect
app = Flask(__name__)
app.secret_key = 'user'

load_dotenv()
CONSUMER_API_KEY = os.environ.get("CONSUMER_API_KEY")
CONSUMER_SECRET_API_KEY = os.environ.get("CONSUMER_SECRET_API_KEY")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

CALLBACK_URL = "http://127.0.0.1:8000/auth"
auth = tp.OAuthHandler(CONSUMER_API_KEY, CONSUMER_SECRET_API_KEY, CALLBACK_URL)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET'])
def login():
    try:
        redirect_url = auth.get_authorization_url()
    except tp.TweepError as e:
        print(e)
    session['request_token'] = auth.request_token
    return redirect(redirect_url)


@app.route('/auth', methods=['GET'])
def authorize():
    api = tp.API(auth)
    user_id = api.me().screen_name
    fav_tweets = api.favorites(user_id, count=10)
    url_pattern = re.compile("https://")
    text_only_tweets = []
    for tweet in fav_tweets:
        if not(url_pattern.search(tweet.text)):
            text_only_tweets.append(tweet)
    return render_template('result.html', twitter_id=user_id, fav_tweets=text_only_tweets)


if __name__ == "__main__":
    app.run(debug=True, port=8000, threaded=True)
