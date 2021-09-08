import os
import re
import time
import tweepy as tp
from libs import rakuten_api, recommend
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect
app = Flask(__name__)
app.secret_key = "asPdljfaasdu3lv"

load_dotenv()
CONSUMER_API_KEY = os.environ.get("CONSUMER_API_KEY")
CONSUMER_SECRET_API_KEY = os.environ.get("CONSUMER_SECRET_API_KEY")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

CALLBACK_URL = "http://127.0.0.1:8000/result"
# CALLBACK_URL="https://young-dawn-36523.herokuapp.com/favorites"

path_to_dict = "./libs/data/mecab/dic/ipadic"
path_to_d2v_model = "./libs/data/Doc2Vec.model"
path_to_aozora = "./libs/data/aozora.csv"


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/test")
def test():
    sample_titles_and_authors = {
            "人間失格": "太宰治",
            "陰翳礼讃": "谷崎潤一郎",
            "変身": "フランツ カフカ",
            "銀河鉄道の夜": "宮沢賢治",
            "風の歌を聴け": "村上春樹",
            "パプリカ": "筒井康隆"
            }
    books_info = []
    for book_title, author in sample_titles_and_authors.items():
        book_info = rakuten_api.getBookInfoFromTitleAndAuthor(book_title, author)
        if (book_info):
            books_info.append(book_info)
        time.sleep(0.2)
    return render_template('result.html', books_info=books_info)


@app.route("/result")
def result():
    verifier = request.args.get('oauth_verifier')
    auth = tp.OAuthHandler(CONSUMER_API_KEY, CONSUMER_SECRET_API_KEY)
    token = session['request_token']
    session.pop('request_token', None)
    auth.request_token = token

    try:
        auth.get_access_token(verifier)
    except tp.TweepError as e:
        print(vars(e))

    api = tp.API(auth)
    user_id = api.me().screen_name
    results = recommend.getMostSimilarBookTitlesFromTweet(user_id, path_to_dict, path_to_d2v_model, path_to_aozora)
    books_info = []
    for item in results:
        title = item[1]
        author = item[2]
        book_info = rakuten_api.getBookInfoFromTitleAndAuthor(title, author)
        if (book_info):
            books_info.append(book_info)
        time.sleep(0.2)
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


"""
@app.route('/favorites', methods=['GET'])
def favorites():
    favorite_tweets = getFavorites()
    return render_template('favorites.html', tweets=favorite_tweets)
"""



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
