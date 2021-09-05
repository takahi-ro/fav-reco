import requests


APPLICATION_ID = "1095524729477042360"


# ISBNを引数に渡すと，その本に関する情報を辞書で返す
def getBookInfoFromISBN(isbn):
    api_url = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
    params = {
            "format": "json",
            "applicationId": APPLICATION_ID,
            "isbn": isbn,
            "hits": 1,
            "sort": "sales"
            }
    results_json = requests.get(api_url, params).json()
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


# ISBNを引数に渡すと，その本に関する情報を辞書で返す
def getBookInfoFromTitleAndAuthor(title, author):
    api_url = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
    params = {
            "format": "json",
            "applicationId": APPLICATION_ID,
            "title": title,
            "author": author,
            "size": 2,
            "hits": 1,
            "sort": "sales"
            }
    results_json = requests.get(api_url, params).json()
    
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
