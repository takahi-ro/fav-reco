from gensim.models.doc2vec import Doc2Vec
import pandas as pd
from dotenv import load_dotenv
import MeCab
import unicodedata
import string
import os
import re
import tweepy as tp
import pprint


# MeCabの辞書にNEologdを指定。
# mecabは携帯素解析用、wakatiは分かち書き用
mecab = MeCab.Tagger("-d C:/neologd")
wakati = MeCab.Tagger(r'-Owakati -d C:/neologd')

# 形態素解析を行う関数を定義
# ファイルを入力するとファイルを出力し、文字列を渡すと文字列を返します。引数fileで変更します。  
# 単に分かち書きしたいだけの場合は引数にmecab=wakatiとすると実現できます。
def MecabMorphologicalAnalysis(path='./text.txt', output_file='wakati.txt', mecab=mecab, file=False):
    mecab_text = ''
    if file:
        with open(path) as f:
            for line in f:
                mecab_text += mecab.parse(line)
        with open(output_file, 'w') as f:
            print(mecab_text, file=f)
    else:
        for path in path.split('\n'):
            mecab_text += mecab.parse(path)
        return mecab_text

# 記号文字は分析をするにあたって邪魔になるため、記号を取り除く関数を定義します。
# 下に示すAozora_table関数の中で使います。
def symbol_removal(soup):
    soup = unicodedata.normalize("NFKC", soup)
    exclusion = "「」『』【】、。・" + "\n" + "\r" + "\u3000"
    soup = soup.translate(str.maketrans("", "", string.punctuation  + exclusion))
    return soup

def get_favs(user_id):
    load_dotenv()
    CONSUMER_API_KEY = "qPMLPTw5wWFbMsOz0JdrPxqcS"
    CONSUMER_SECRET_API_KEY = "1VlzfvR3AIyaXCe1IDPCr2lDYaufSehNH4PJ5EclgxEFZXc9T5"
    ACCESS_TOKEN = "1361165452953620485-OgoQLVB3W15F1Bn3B130QCreJgbhXN"
    ACCESS_TOKEN_SECRET = "lC99VaFgVsWyk9ZUEMZHiY6BimRsG4Y2MXFtsV0osvDoa"
    auth = tp.OAuthHandler(CONSUMER_API_KEY, CONSUMER_SECRET_API_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tp.API(auth)

    fav_tweets = api.favorites(user_id, count=50)

    url_pattern = re.compile("https://")
    fav_tweet_texts = [fav_tweet.text for fav_tweet in fav_tweets if not url_pattern.search(fav_tweet.text)]
    fav_tweet_texts = [symbol_removal(t) for t in fav_tweet_texts]
    # fav_tweets_text = symbol_removal("".join(fav_tweets_text))
    # fav_row =  pd.Series([user_id, "likes", fav_tweets_text], index=df.columns)
    return fav_tweet_texts

m = Doc2Vec.load('C:/Users/S2/Documents/M2/つぶやき書店/fav-reco/model/new_doc2vec_ver02.model')

df = pd.read_csv('C:/Users/S2/Documents/M2/つぶやき書店/fav-reco/textdata_ver02.csv')
titles = df["title"]


tweets = get_favs("@kai_washino")
wakati_tweets = [MecabMorphologicalAnalysis(t, mecab=wakati) for t in tweets]

# リストに変換
sentences = []
for text in wakati_tweets:
    text_list = text.split(' ')
    sentences.append(text_list)

reccomend = []
for idx, s in enumerate(sentences):
    most_similar = m.docvecs.most_similar([m.infer_vector(s)], topn=1)
    reccomend.append([tweets[idx], titles[most_similar[0][0]]])

#pprint.pprint(reccomend)
