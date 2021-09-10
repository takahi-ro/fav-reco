import pandas as pd
import MeCab
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import re




# MeCabの辞書にNEologdを指定。
# mecabは携帯素解析用、wakatiは分かち書き用
mecab = MeCab.Tagger("-d C:/neologd")
wakati = MeCab.Tagger(r'-Owakati -d C:/neologd')


df = pd.read_csv("C:/Users/S2/Documents/M2/つぶやき書店/washino/textdata_ver02.csv")


"""
texts = []
text_remove_pp = mecab.parse(df['text'][0])
words = []
lines = text_remove_pp.split('\n')
for line in lines:
    items = re.split('[\t,]',line)
    print(items)
    if len(items) >= 2 and items[1] == '助詞':
        continue
    if len(items) >= 2 and items[1] == '連体詞':
        continue
    if len(items) >= 2 and items[2] == '代名詞':
        continue
    if len(items) >= 2 and items[0] == 'こと':
        continue
    words.append(items[0])
text = (' '.join(words))

texts.append(wakati.parse(text))
print(texts)
"""

#わかち書き
text_remove_pp = []
texts = []
for i in range(len(df)):
    
    text_remove_pp = mecab.parse(df['text'][i])
    words = []
    lines = text_remove_pp.split('\n')
    for line in lines:
        items = re.split('[\t,]',line)
        if len(items) >= 2 and items[1] == '助詞':
            continue
        if len(items) >= 2 and items[1] == '連体詞':
            continue
        if len(items) >= 2 and items[2] == '代名詞':
            continue
        if len(items) >= 2 and items[0] == 'こと':
            continue
        words.append(items[0])
    text = (' '.join(words))
    
    texts.append(wakati.parse(text))
    print(i)

# リストに変換
sentences = []
for text in texts:
    text_list = text.split(' ')
    sentences.append(text_list)

documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(sentences)]
model = Doc2Vec(documents, vector_size=100, window=5, min_count=1)
model.save("C:/Users/S2/Documents/M2/つぶやき書店/fav-reco/model/new_doc2vec_ver03.model")
