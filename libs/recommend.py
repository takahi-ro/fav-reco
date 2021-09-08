from gensim.models.doc2vec import Doc2Vec
import pandas as pd
from dotenv import load_dotenv
import MeCab
import unicodedata
import string
import os
import re
import tweepy as tp


def textsToWakatiList(texts, path_to_dict):
    wakati = MeCab.Tagger("-Owakati -d " + path_to_dict)
    results = []
    for text in texts:
        results.append(wakati.parse(text))
    return results


def removeSymbol(soup):
    soup = unicodedata.normalize("NFKC", soup)
    exclusion = "「」『』【】、。・" + "\n" + "\r" + "\u3000"
    soup = soup.translate(str.maketrans("", "", string.punctuation  + exclusion))
    return soup


def getFavs(user_id):
    load_dotenv()
    CONSUMER_API_KEY = os.environ.get("CONSUMER_API_KEY")
    CONSUMER_SECRET_API_KEY = os.environ.get("CONSUMER_SECRET_API_KEY")
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
    auth = tp.OAuthHandler(CONSUMER_API_KEY, CONSUMER_SECRET_API_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tp.API(auth)

    fav_tweets = api.favorites(user_id, count=10)

    url_pattern = re.compile("https://")
    fav_tweet_texts = [fav_tweet.text for fav_tweet in fav_tweets if not url_pattern.search(fav_tweet.text)]
    fav_tweet_texts = [removeSymbol(t) for t in fav_tweet_texts]
    return fav_tweet_texts


def getMostSimilarBookTitlesFromTweet(twitter_id, path_to_dict, path_to_d2v_model, path_to_aozora):

    m = Doc2Vec.load(path_to_d2v_model)
    df = pd.read_csv(path_to_aozora)
    titles = df["title"]
    authors = df["author"]
    tweets = getFavs(twitter_id)
    wakati_tweets = textsToWakatiList(tweets, path_to_dict)

    sentences = []
    for text in wakati_tweets:
        text_list = text.split(' ')
        sentences.append(text_list)

    recommend = []
    for idx, s in enumerate(sentences):
        most_similar = m.dv.most_similar([m.infer_vector(s)], topn=1)
        recommend.append([tweets[idx], titles[most_similar[0][0]], authors[most_similar[0][0]]])
    return recommend


"""
path_to_d2v_model = "./data/Doc2Vec.model"
path_to_aozora = "./data/aozora.csv"
path_to_dict = "./data/mecab/dic/ipadic"
results = getMostSimilarBookTitlesFromTweet("@unacceptablee2", path_to_dict, path_to_d2v_model, path_to_aozora)
for item in results:
    print(item[1], item[2])
"""
