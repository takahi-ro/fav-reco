
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from sklearn.cluster import KMeans
import sys
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import recc_from_one_tweet 
from recc_from_one_tweet import MecabMorphologicalAnalysis, get_favs
import collections

def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

df = pd.read_csv('/Users/jinya/Desktop/fav-reco/textdata.csv')
titles = df["title"]

# モデルを読み込む
# モデルは絶対パスで指定してください
m = Doc2Vec.load('/Users/jinya/Desktop/fav-reco/model/new_doc2vec.model')

# ベクトルをリストに格納
vectors_list = [m.docvecs[n] for n in range(len(m.docvecs))]

# ドキュメント番号のリスト
doc_nums = range(len(m.docvecs))
print(doc_nums)

# クラスタリング設定
# クラスター数を変えたい場合はn_clustersを変えてください
n_clusters = 8
kmeans_model = KMeans(n_clusters=n_clusters, verbose=1,
                      random_state=1, n_jobs=-1)

# クラスタリング実行
kmeans_model.fit(vectors_list)

# クラスタリングデータにラベル付け
labels = kmeans_model.labels_
print(np.array(vectors_list).shape)

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

tweets = get_favs("@odmishien")
wakati_tweets = [MecabMorphologicalAnalysis(t, mecab=recc_from_one_tweet.wakati) for t in tweets]

# リストに変換
sentences = []
for text in wakati_tweets:
    text_list = text.split(' ')
    sentences.append(text_list)

tweet_vector_list = [m.infer_vector(t, epochs = 50) for t in sentences]

#　ツイートごとに最も類似しているクラスタを求める
sim_cluster = []
cluster_tweet = defaultdict(list)
for t_v in tweet_vector_list:
    sim_dict = {}
    for c, v in cluster_vector.items():
        sim_dict[c] = cos_sim(v, t_v)
    sorted_sim = sorted(sim_dict.items(), key=lambda x:x[1])[0][0]
    sim_cluster.append(sorted_sim)
    cluster_tweet[sorted_sim].append(t_v)

count_cluster = collections.Counter(sim_cluster)   #　クラスタの出現回数（辞書型）
reccomend_cluster = max(count_cluster, key = count_cluster.get)

print("あなたのクラスタは"+ str(reccomend_cluster) + "です")


reccomend_doc = []
for t_v in cluster_tweet[reccomend_cluster]:
    sim_docs = {}
    for doc_num in cluster_to_docs[reccomend_cluster]:
        sim_docs[doc_num] = cos_sim(t_v, vectors_list[doc_num])
    reccomend_doc.append(df["title"][max(sim_docs, key=sim_docs.get)])

print(reccomend_doc)

