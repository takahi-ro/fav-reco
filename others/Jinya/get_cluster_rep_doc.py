from gensim.models.doc2vec import Doc2Vec
from sklearn.cluster import KMeans
from collections import defaultdict
import numpy as np
import pandas as pd

def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

df = pd.read_csv('/Users/jinya/Desktop/fav-reco/textdata.csv')

# モデルを読み込む
# モデルは絶対パスで指定してください
m = Doc2Vec.load('/Users/jinya/Desktop/fav-reco/model/new_doc2vec.model')

#ベクトルをリストに格納
vectors_list=[m.dv[n] for n in range(len(m.dv))]

#ドキュメント番号のリスト
doc_nums=range(len(m.dv))

#クラスタリング設定
#クラスター数を変えたい場合はn_clustersを変えてください
n_clusters = 8
kmeans_model = KMeans(n_clusters=n_clusters, verbose=1, random_state=1)

#クラスタリング実行
kmeans_model.fit(vectors_list)

#クラスタリングデータにラベル付け
labels=kmeans_model.labels_
import collections
count = collections.Counter(labels)
print(count)

cluster_vector = {}
for i in range(n_clusters):
    cluster_vector[i] = kmeans_model.cluster_centers_[i]

#ラベルとドキュメント番号の辞書づくり
cluster_to_docs = defaultdict(list)
for cluster_id, doc_num in zip(labels, doc_nums):
    cluster_to_docs[cluster_id].append(doc_num)

cluster_docs = defaultdict(list)
for c in range(n_clusters):
    c_v = cluster_vector[c]
    sims = {}
    for doc_num in cluster_to_docs[c]:
        sim = cos_sim(vectors_list[doc_num],c_v)
        sims[doc_num] = sim
    docs_sorted_sims = [s[0] for s in sorted(sims.items(), key=lambda i: i[1], reverse=True)[0:10]]
    cluster_docs[c].append(docs_sorted_sims)

for c in range(n_clusters):
    print("クラスタ：" + str(c))
    for doc_num in cluster_docs[c]:
        print(df["title"][doc_num])
    print("------------------------")







