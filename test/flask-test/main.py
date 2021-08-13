import os
import re
import tweepy as tp
from dotenv import load_dotenv
from flask import Flask, render_template, request
app = Flask(__name__)

load_dotenv()
CONSUMER_API_KEY = os.environ.get("CONSUMER_API_KEY")
CONSUMER_SECRET_API_KEY = os.environ.get("CONSUMER_SECRET_API_KEY")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

auth = tp.OAuthHandler(CONSUMER_API_KEY, CONSUMER_SECRET_API_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tp.API(auth)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/", methods=['POST'])
def get_form():
    twitter_id = request.form['user-id']
    fav_tweets = api.favorites(twitter_id, count=50)
    url_pattern = re.compile("https://")
    text_only_tweets = []
    for tweet in fav_tweets:
        if not(url_pattern.search(tweet.text)):
            text_only_tweets.append(tweet)
    return render_template('result.html', twitter_id=twitter_id, fav_tweets=text_only_tweets)


if __name__ == "__main__":
    app.run(debug=True, port=8000, threaded=True)
