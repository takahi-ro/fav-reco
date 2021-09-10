from gensim import corpora
from gensim import models
import pandas as pd
import string
import MeCab
import unicodedata
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import os
import re
import collections




def Wakati (df):
    #わかち書き
    texts = []
    for i in range(len(df)):
        texts.append(wakati.parse(df['text'][i]))
        #print(i)
    # リストに変換
    sentences = []
    for text in texts:
        text_list = text.split(' ')
        sentences.append(text_list)



wakati = MeCab.Tagger(r'-Owakati -d C:/neologd')

# 青空文庫からスクレイピングしてきた文庫情報を取得
df = pd.read_csv('C:/Users/S2/Documents/M2/つぶやき書店/fav-reco/textdata.csv')
title = df["title"]

# クラスターを読み込む

cluster_df = pd.read_csv('C:/Users/S2/documents/M2/つぶやき書店/washino/cluster.csv', header=None, names=['id', 'cluster'])
#m = Doc2Vec.load('doc2vec.model')

#titleid = []
for i in range(12):
    titleid = (cluster_df[cluster_df.cluster == i+1].id)
print(titleid.iloc[:,1])
#print(title)

"""

def genre_estimation(cluster_word):
    # 単語の出現回数
    t_counter = [{},{},{},{},{},{},{},{}]
    for c, words in enumerate(cluster_word):
        count = collections.Counter(words)
        t_counter[c] = count
      
    # クラスタ内の単語総数
    sum_in_c = []
    for count in t_counter:
        num = 0
    for i in count.values():
        num += i
        sum_in_c += [num]
    # tf計算
    tf_c = [{},{},{},{},{},{},{},{}]
    for i, count in enumerate(t_counter):
        for key, value in count.items():
            tf_c[i][key] = value/sum_in_c[i]
            # 全ての単語の辞書を作成
            all_word = {}
    for c in cluster_word:
      for word in c:
    #all_word[word] = 0
    # 単語がいくつの文書に出いているか
    for docs in docs_cluster:
      words = docs[1].split(" ")
    for word in set(words):
    all_word[word] += 1
    # idfの計算
    import math
    idf_word = {}
    for key, i in all_word.items():
      idf_word[key] = math.log(2000/i + 1)
    # tf-idfの計算
    tf_idf = [{},{},{},{},{},{},{},{}]
    for i, c in enumerate(tf_c):
    for key, value in c.items():
    tf_idf[i][key] = value * idf_word[key]

"""