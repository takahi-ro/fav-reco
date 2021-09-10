import requests
from jpndlpy import JapanNdlClient


jndlclient = JapanNdlClient()
response = jndlclient.search_text(title="斜陽",  mediatype=1, cnt=2).to_json()

print(response)
for k, v in response["items"][0].items():
    print(k, v)

# print(response["items"][0])


"""
sru_url = "https://iss.ndl.go.jp/api/sru"
params = {
        "operation": "searchRetrieve",
        "maximumRecords": 1,
        "query": {
            "title=人間失格",
            "creator=太宰治"
            }
        }

result = requests.get(sru_url, params)
print(result.url)
# print(result.text)
"""
