import os
import re
import requests
import tweepy as tp
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect
app = Flask(__name__)
app.secret_key = "asPdljfaasdu3lv"

load_dotenv()
CONSUMER_API_KEY = os.environ.get("CONSUMER_API_KEY")
CONSUMER_SECRET_API_KEY = os.environ.get("CONSUMER_SECRET_API_KEY")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
APPLICATION_ID = "1095524729477042360"

# CALLBACK_URL = "http://127.0.0.1:8000/favorites"
CALLBACK_URL="https://young-dawn-36523.herokuapp.com/favorites"


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/result")
def result():
    search_keyword = "息吹"
    api_url = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
    params = {
            "format": "json",
            "title": search_keyword,
            "applicationId": APPLICATION_ID,
            "hits": 1,
            "sort": "sales"
            }
    results = requests.get(api_url, params).json()
    title = results['Items'][0]['Item']['title']
    image = results['Items'][0]['Item']['mediumImageUrl']
    caption = results['Items'][0]['Item']['itemCaption']
    data = results['Items'][0]['Item']['salesDate']
    rakuten_url = results['Items'][0]['Item']['itemUrl']
    return render_template('result.html', book_title=title, book_image=image, book_caption=caption, sales_date=data, item_url=rakuten_url)

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
    return render_template('favorites.html', twitter_id=user_id, fav_tweets=text_only_tweets)


if __name__ == "__main__":
    app.run(debug=False, port=8000, threaded=True)
