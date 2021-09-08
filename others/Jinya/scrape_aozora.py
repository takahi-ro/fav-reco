from bs4 import BeautifulSoup
import requests
import pandas as pd
import string
import unicodedata

def Aozora_table(n=30):
    url = "https://www.aozora.gr.jp/access_ranking/2019_xhtml.html"
    res = requests.get(url)
    res.encoding = 'shift-jis'
    soup = BeautifulSoup(res.content, "html.parser")

    url_list = [url["href"] for i, url in enumerate(soup.find_all("a", target="_blank")) if i < n]

    title = []
    author = []
    text = []
    for url in url_list:
        res = requests.get(url)
        url_start = url[:37]
        res.encoding = 'shift-jis'
        soup = BeautifulSoup(res.content, "html.parser")
        for i, a in enumerate(soup.find_all("a")):
            if i == 7:
                url_end = a["href"][1:]
        url = url_start + url_end
        res = requests.get(url)
        res.encoding = 'shift-jis'
        soup = BeautifulSoup(res.content, "html.parser")
        title.append(soup.find("h1").string)
        author.append(soup.find("h2").string)
        for tag in soup.find_all(["rt", "rp"]):
            tag.decompose()
        soup = soup.find("div",{'class': 'main_text'}).get_text()
        text.append(symbol_removal(soup))
    df = pd.DataFrame({'title': title, 'author': author, 'text': text})
    return df

def symbol_removal(soup):
    soup = unicodedata.normalize("NFKC", soup)
    exclusion = "「」『』【】、。・" + "\n" + "\r" + "\u3000"
    soup = soup.translate(str.maketrans("", "", string.punctuation  + exclusion))
    return soup

df = Aozora_table(50)

df.to_csv('../data/aozora.csv')


