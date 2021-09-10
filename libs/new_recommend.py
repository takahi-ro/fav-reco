import MeCab
from gensim.models.doc2vec import Doc2Vec
from sklearn.cluster import KMeans
from collections import defaultdict
import numpy as np
import pandas as pd
import collections
import tweepy as tp
import os
import re
import unicodedata
import string
from dotenv import load_dotenv


def textsToWakatiList(texts, path_to_dict):
    wakati = MeCab.Tagger("-Owakati -d " + path_to_dict)
    results = []
    for text in texts:
        results.append(wakati.parse(text))
    return results


def removeSymbol(soup):
    soup = unicodedata.normalize("NFKC", soup)
    exclusion = "〔〕「」『』【】、。・" + "\n" + "\r" + "\u3000"
    soup = soup.translate(str.maketrans("", "", string.punctuation  + exclusion))
    return soup


def getFavs(user_id, count):
    load_dotenv()
    CONSUMER_API_KEY = os.environ.get("CONSUMER_API_KEY")
    CONSUMER_SECRET_API_KEY = os.environ.get("CONSUMER_SECRET_API_KEY")
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
    auth = tp.OAuthHandler(CONSUMER_API_KEY, CONSUMER_SECRET_API_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tp.API(auth)

    fav_tweets = api.favorites(user_id, count)

    url_pattern = re.compile("https://")
    fav_tweet_texts = [fav_tweet.text for fav_tweet in fav_tweets if not url_pattern.search(fav_tweet.text)]
    fav_tweet_texts = [removeSymbol(t) for t in fav_tweet_texts]
    return fav_tweet_texts

def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def getMostSimilerClusterOfFavs(twitter_id, path_to_textdata, path_to_dict, path_to_model):
    m = Doc2Vec.load(path_to_model)
    df = pd.read_csv(path_to_textdata)

    vectors_list = [m.dv[n] for n in range(len(m.dv))]
    doc_nums = range(len(m.dv))
    n_clusters = 8
    kmeans_model = KMeans(n_clusters=n_clusters, verbose=1,
                          random_state=1, n_jobs=-1)
    kmeans_model.fit(vectors_list)
    labels = kmeans_model.labels_
    # print(np.array(vectors_list).shape)

    # ラベルとドキュメント番号の辞書づくり
    cluster_to_docs = defaultdict(list)
    for cluster_id, doc_num in zip(labels, doc_nums):
        cluster_to_docs[cluster_id].append(doc_num)

    # クラスタごとの文書ベクトルの平均値を求める
    cluster_vector = {}
    for c in cluster_to_docs:
        _cluster_vector = np.zeros(100)
        for doc_num in cluster_to_docs[c]:
            doc_vector = np.array(vectors_list[doc_num])
            _cluster_vector += doc_vector
        _cluster_vector /= len(cluster_to_docs[c])
        cluster_vector[c] = _cluster_vector

    favorite_tweets = getFavs(twitter_id, 100)
    wakati_tweets = textsToWakatiList(favorite_tweets, path_to_dict)
    sentences = []
    for tweet in wakati_tweets:
        sentences.append(tweet.split(' '))

    tweet_vector_list = [m.infer_vector(t, epochs=50) for t in sentences]

    # ツイートごとに最も類似しているクラスタを求める
    sim_cluster = []
    cluster_tweet = defaultdict(list)
    for t_v in tweet_vector_list:
        sim_dict = {}
        for c, v in cluster_vector.items():
            sim_dict[c] = cos_sim(v, t_v)
        sorted_sim = sorted(sim_dict.items(), key=lambda x: x[1])[0][0]
        sim_cluster.append(sorted_sim)
        cluster_tweet[sorted_sim].append(t_v)

    count_cluster = collections.Counter(sim_cluster)
    reccomend_cluster = max(count_cluster, key=count_cluster.get)

    print("Your cluster:", reccomend_cluster)

    result = {}
    for t_v in cluster_tweet[reccomend_cluster]:
        sim_docs = {}
        for doc_num in cluster_to_docs[reccomend_cluster]:
            sim_docs[doc_num] = cos_sim(t_v, vectors_list[doc_num])
        title = df["title"][max(sim_docs, key=sim_docs.get)]
        author = df["author"][max(sim_docs, key=sim_docs.get)]
        base_book = df["original"][max(sim_docs, key=sim_docs.get)]
        result[title] = author
    return result
