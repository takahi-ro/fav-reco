import os
import re
import tweepy as tp
from libs import rakuten_api
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect
app = Flask(__name__)
app.secret_key = "asPdljfaasdu3lv"

load_dotenv()
CONSUMER_API_KEY = os.environ.get("CONSUMER_API_KEY")
CONSUMER_SECRET_API_KEY = os.environ.get("CONSUMER_SECRET_API_KEY")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

CALLBACK_URL = "http://127.0.0.1:8000/favorites"
# CALLBACK_URL="https://young-dawn-36523.herokuapp.com/favorites"


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/result")
def result():
    sample_titles_and_authors = {
            "人間失格": "太宰治",
            "陰翳礼讃": "谷崎潤一郎",
            "変身": "フランツ カフカ",
            "銀河鉄道の夜": "宮沢賢治",
            "羅生門": "芥川龍之介",
            "山椒大夫": "森鴎外"
            }
    books_info = {}
    for k, v in sample_titles_and_authors.items():
        book_info = rakuten_api.getBookInfoFromTitleAndAuthor(k, v)
        if (book_info["isFound"]):
            books_info[k] = book_info["image"]
    return render_template('result.html', books_info=books_info)


@app.route('/login', methods=['GET'])
def login():
    auth = tp.OAuthHandler(CONSUMER_API_KEY, CONSUMER_SECRET_API_KEY, CALLBACK_URL)
    try:
        redirect_url = auth.get_authorization_url()
        session['request_token'] = auth.request_token
    except tp.TweepError as e:
        print(vars(e))
    return redirect(redirect_url)


@app.route('/favorites', methods=['GET'])
def favorites():
    favorite_tweets = getFavorites()
    return render_template('favorites.html', tweets=favorite_tweets)

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


if __name__ == "__main__":
    app.run(debug=False, port=8000, threaded=True)
