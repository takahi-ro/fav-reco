import os
import re
import requests
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

@app.route("/result")
def result():
    sample_isbn = "4041099153"
    book_info = getBookInfoFromISBN(sample_isbn)
    return render_template('result.html', book_info=book_info)


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
    return render_template('favorites.html', twitter_id=user_id, fav_tweets=text_only_tweets)

def getBookInfoFromISBN(isbn):
    APPLICATION_ID = "1095524729477042360"
    api_url = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
    params = {
            "format": "json",
            "applicationId": APPLICATION_ID,
            "isbn": isbn,
            "hits": 1,
            "sort": "sales"
            }
    results_json = requests.get(api_url, params).json()
    book_info = results_json['Items'][0]['Item']
    results = {
            "title": book_info["title"],
            "image": book_info["mediumImageUrl"],
            "author": book_info["author"],
            "caption": book_info["itemCaption"],
            "sales_date": book_info["salesDate"],
            "publisher": book_info["publisherName"],
            "rakuten_url": book_info["itemUrl"]
            }
    return results

if __name__ == "__main__":
    app.run(debug=True, port=8000, threaded=True)
