from gensim.models.doc2vec import Doc2Vec
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
import pandas as pd
import numpy as np


df = pd.read_csv('C:/Users/S2/Documents/M2/つぶやき書店/fav-reco/textdata_ver02.csv')
titles = df["title"]

# モデルを読み込む
# モデルは絶対パスで指定してください
m = Doc2Vec.load('C:/Users/S2/Documents/M2/つぶやき書店/fav-reco/model/new_doc2Vec_ver03.model')

# ベクトルをリストに格納
vectors_list = [m.docvecs[n] for n in range(len(m.docvecs))]
print(vectors_list[0])

# ドキュメント番号のリスト
doc_nums = range(len(m.docvecs))


class_data_list = []
result_class_num = 0



# 2〜データ個数の9割りまでクラスタ数を指定する
loop_num = 30
for class_num in range(2, loop_num):
    # クラスタ分類
    km = KMeans(n_clusters=class_num,
            init='k-means++',     
            n_init=10,
            max_iter=300,
            random_state=0)
    y_km = km.fit_predict(vectors_list) 
    
    cluster_labels = np.unique(y_km) 

    # 配列の数
    n_clusters = cluster_labels.shape[0] 

    #シルエット係数を計算
    silhouette_vals = silhouette_samples(vectors_list,y_km,metric='euclidean')
    
    # クラスタ内のデータ数
    sil=[]
    for i,c in enumerate(cluster_labels):
        c_silhouette_vals=silhouette_vals[y_km==c]
        sil.append(len(c_silhouette_vals))
    
    # クラスタ内のデータ数の差がデータ数の2割以下であれば分割できたとみなす
    data_diff = int(len(doc_nums) * 0.2)
    data_diff_flg = max(sil)-min(sil) < data_diff
    # クラスタ内のシルエット係数平均値
    ave_silhouette_vals = np.average(silhouette_vals)
    
    class_data_list.append({'class_num':class_num, 'data_diff':data_diff_flg, 'ave':ave_silhouette_vals})
    print(i)
        
max_ave = 0
for class_data in class_data_list:
    if  (max_ave < class_data['ave']):
        max_ave = class_data['ave']
        result_class_num = class_data['class_num']
        print("max")
        
print("rusult:", result_class_num)

