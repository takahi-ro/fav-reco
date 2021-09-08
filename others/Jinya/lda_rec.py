import pandas as pd
import itertools
import random
import logging
import MeCab
from gensim import corpora, models
import numpy as np
from scipy.special import digamma
import tweepy as tp
from dotenv import load_dotenv

# Vis
from tqdm import tqdm
from wordcloud import WordCloud
from PIL import Image
import matplotlib
import matplotlib.pylab as plt
font = {'family': 'TakaoGothic'}
matplotlib.rc('font', **font)

# MeCabの辞書にNEologdを指定。
# mecabは携帯素解析用、wakatiは分かち書き用
mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
wakati = MeCab.Tagger("-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")

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

#青空文庫データの読み取り
df = pd.read_csv('/Users/jinya/Desktop/fav-reco/test/Jinya/data/aozora.csv')
texts = []
for i in range(len(df)):
    texts.append(MecabMorphologicalAnalysis(df['text'][i], mecab=wakati).split())

#単語とIDのマッピング
d = corpora.Dictionary(texts)

# 使われいる文書の数がno_belowより少ない単語を無視し、no_aboveの割合以上の文書に出てくる単語を無視
# compactifyでIDを振り直してコンパクトに
d.filter_extremes(no_below=5, no_above=0.2)
d.compactify()

corpus = [d.doc2bow(w) for w in texts]
test_size = int(len(corpus) * 0.1)
test_corpus = corpus[:test_size]
train_corpus = corpus[test_size:]

#Metrics for Topic Models
start = 2
limit = 22
step = 1

coherence_vals = []
perplexity_vals = []

for n_topic in tqdm(range(start, limit, step)):
    lda_model = models.ldamodel.LdaModel(corpus=corpus, id2word=d, num_topics=n_topic, random_state=0)
    perplexity_vals.append(np.exp2(-lda_model.log_perplexity(corpus)))
    coherence_model_lda = models.CoherenceModel(model=lda_model, texts=texts, dictionary=d, coherence='c_v')
    coherence_vals.append(coherence_model_lda.get_coherence())

# evaluation
x = range(start, limit, step)

fig, ax1 = plt.subplots(figsize=(12,5))

# coherence
c1 = 'darkturquois'
ax1.plot(x, coherence_vals, 'o-', color=c1)
ax1.set_xlabel('Num Topics')
ax1.set_ylabel('Coherence', color=c1); ax1.tick_params('y', colors=c1)

# perplexity
c2 = 'slategray'
ax2 = ax1.twinx()
ax2.plot(x, perplexity_vals, 'o-', color=c2)
ax2.set_ylabel('Perplexity', color=c2); ax2.tick_params('y', colors=c2)

# Vis
ax1.set_xticks(x)
fig.tight_layout()
plt.show()

# save as png
# plt.savefig('metrics.png') 

# # logging.basicConfig(format='%(message)s', level=logging.INFO)
# lda = models.ldamodel.LdaModel(corpus=corpus, id2word=d, num_topics=10)

# N = sum(count for doc in test_corpus for id, count in doc)
# print("N: ",N)

# perplexity = np.exp2(-lda.log_perplexity(test_corpus))
# print("perplexity:", perplexity)

# def get_topic_words(topic_id):
#     for t in lda.get_topic_terms(topic_id):
#         print("{}: {}".format(d[t[0]], t[1]))
# for t in range(10):
#     print("Topic # ",t)
#     get_topic_words(t)
#     print("\n")


