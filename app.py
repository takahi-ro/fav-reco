import os
import time
import tweepy as tp
from libs import get_book_info, recommend
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect


app = Flask(__name__)
app.secret_key = os.urandom(16)

load_dotenv()
CONSUMER_API_KEY = os.environ.get("CONSUMER_API_KEY")
CONSUMER_SECRET_API_KEY = os.environ.get("CONSUMER_SECRET_API_KEY")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
APPLICATION_ID = os.environ.get("APPLICATION_ID")

CALLBACK_URL = "http://127.0.0.1:8000/result"
# CALLBACK_URL = "http://tsubuyaki-syoten.herokuapp.com/result"

path_to_dict = "./libs/data/mecab/dic/ipadic"
path_to_d2v_model = "./libs/data/Doc2Vec.model"
path_to_aozora = "./libs/data/aozora.csv"
path_to_dummy = "./static/img/dummy-book"
path_to_book = "./static/img/book.png"

dummy_img = os.listdir(path_to_dummy)


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
    index = 0
    for book_title, author in sample_titles_and_authors.items():
        book_info = get_book_info.getBookInfoFromTitleAndAuthor(book_title, author, APPLICATION_ID)
        if (book_info):
            book_info["mediumImageUrl"] = path_to_dummy + "/" + dummy_img[index]
            books_info.append(book_info)
            index += 1
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
    for title, author in results.items():
        book_info = get_book_info.getBookInfoFromTitle(title)
        print(title, author, book_info)
        if (book_info):
            books_info.append(book_info)
        """
        base_book = get_book_info.getAozoraBaseBookFromTitleAndAuthor(title, author)
        if (base_book):
            book_info = get_book_info.getBookInfoFromBaseBookTitle(base_book)
            if (book_info):
                books_info.append(book_info)
        """
        time.sleep(0.2)
    return render_template('result.html', books_info=books_info)


@app.route('/login', methods=['GET'])
def login():
    auth = tp.OAuthHandler(CONSUMER_API_KEY, CONSUMER_SECRET_API_KEY, CALLBACK_URL)
    try:
        redirect_url = auth.get_authorization_url()
        session['request_token'] = auth.request_token
    except tp.TweepError as e:
        print("Tweepy Error:", vars(e))
    return redirect(redirect_url)


if __name__ == "__main__":
    app.run(debug=False, port=8000, threaded=True)
