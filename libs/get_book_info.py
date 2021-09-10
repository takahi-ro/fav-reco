import requests

APP_ID = "1095524729477042360"
# ISBNを引数に渡すと，その本に関する情報を辞書で返す
def getBookInfoFromISBN(isbn, APPLICATION_ID):
    rakuten_api_url = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
    params = {
            "format": "json",
            "applicationId": APPLICATION_ID,
            "isbn": isbn,
            "hits": 1,
            "sort": "sales"
            }
    result_json = requests.get(rakuten_api_url, params).json()
    book_info = result_json['Items'][0]['Item']
    result = {
            "title": book_info["title"],
            "image": book_info["mediumImageUrl"],
            "author": book_info["author"],
            "caption": book_info["itemCaption"],
            "sales_date": book_info["salesDate"],
            "publisher": book_info["publisherName"],
            "rakuten_url": book_info["itemUrl"]
            }
    return result


# 文章タイトルと著者名から，本に関する情報を辞書で返す
# 見つからなかった場合は空の辞書を返す
def getBookInfoFromTitleAndAuthor(title, author, APPLICATION_ID):
    rakuten_books_api_url = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
    params = {
            "format": "json",
            "applicationId": APPLICATION_ID,
            "title": title,
            "author": author,
            "size": 0,
            "hits": 30,
            "sort": "reviewCount"
            }
    result = []
    try:
        result_json = requests.get(rakuten_books_api_url, params).json()
        for item in result_json['Items']:
            if (item['Item']['author'] == author) and (item['Item']['title'] == title):
                result.append(item['Item'])
    except Exception as e:
        print("error in getBookInfoFromTitleAndAuthor:", e)
    return result


def getBookInfoFromTitleAndAuthorAndPublisher(title, author, publisher, APPLICATION_ID):
    rakuten_books_api_url = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
    params = {
            "format": "json",
            "applicationId": APPLICATION_ID,
            "title": title,
            "author": author,
            "publisherName": publisher,
            "size": 0,
            "sort": "reviewCount",
            "hits": 30,
            }
    result = []
    try:
        result_json = requests.get(rakuten_books_api_url, params).json()
        print(len(result_json['Items']))
        for item in result_json['Items']:
            if (item['Item']['author'] == author) and (item['Item']['title'] == title) and(item['Item']['publisherName'] == publisher):
                result.append(item['Item'])
    except Exception as e:
        print("error in getBookInfoFromTitleAndAuthor:", e)
    return result


def getAozoraBaseBookFromTitleAndAuthor(title, author):
    api_url = "http://pubserver2.herokuapp.com/api/v0.1/books"
    params = {
            "title": title,
            }
    results = []
    try:
        results = requests.get(api_url, params).json()
    except Exception as e:
        print("error in getAozoraBaseBookFromTitleAndAuthor:", e)
    return results


def getBookInfoFromTitle(title, APPLICATION_ID):
    rakuten_books_api_url = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
    params = {
            "format": "json",
            "applicationId": APPLICATION_ID,
            "title": title,
            "size": 0,
            "hits": 1,
            }
    result = {}
    try:
        result_json = requests.get(rakuten_books_api_url, params).json()
        book_info = result_json['Items'][0]['Item']
        for key, value in book_info.items():
            result[key] = value
    except Exception as e:
        print("error in getBookInfoFromTitle:", e)
    return result


print(getBookInfoFromTitleAndAuthor("人間失格", "太宰治", APP_ID))
