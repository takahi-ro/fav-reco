import requests


APPLICATION_ID = "1095524729477042360"
search_keyword = "息吹"
api_url = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
params = {
        "format": "json",
        "title": search_keyword,
        "applicationId": APPLICATION_ID,
        "hits": 1,
        "sort": "sales"
        }

results = requests.get(api_url, params).json()
# print(results)
print("author:", results['Items'][0]['Item']['author'])
print("title:", results['Items'][0]['Item']['title'])
print("image URL:", results['Items'][0]['Item']['mediumImageUrl'])
print("caption:", results['Items'][0]['Item']['itemCaption'])
print("sales Date:", results['Items'][0]['Item']['salesDate'])
print("item URL:", results['Items'][0]['Item']['itemUrl'])

