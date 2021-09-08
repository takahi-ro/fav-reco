import requests

APPLICATION_ID = "1095524729477042360"

def getBookInfoFromTitleAndAuthor(title, author):
    rakuten_books_api_url = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
    params = {
            "format": "json",
            "applicationId": APPLICATION_ID,
            "title": title,
            "author": author,
            "size": 2,
            "hits": 1,
            }
    results_json = requests.get(rakuten_books_api_url, params).json()
    book_info = results_json['Items'][0]['Item']
    results = {
            "title": book_info["title"],
            "image": book_info["mediumImageUrl"],
            "author": book_info["author"],
            "caption": book_info["itemCaption"],
            "sales_date": book_info["salesDate"],
            "publisher": book_info["publisherName"],
            "rakuten_url": book_info["itemUrl"]
            }
    return results


title = "人間失格"
author = "foo"
try:
    book_info = getBookInfoFromTitleAndAuthor(title, author)
    print(book_info)
except Exception as e:
    print(e)
