import requests


def getAozoraInfo(title):
    url = "https://api.bungomail.com/v0/books"
    params = {
            "作品名": title,
            "limit": 1
            }
    result = {}
    try:
        result_json = requests.get(url, params).json()
        book_info = result_json['books'][0]
        result = {
                "title": book_info["作品名"],
                "mediumImageUrl": "",
                "author": book_info["人物"]["著者"]["姓名"],
                "itemCaption": book_info["書き出し"],
                "salesDate": book_info["公開日"],
                "publisherName": book_info["底本出版社名1"],
                "itemUrl": book_info["XHTML/HTMLファイルURL"]
                }
    except Exception as e:
        print("error in getAozoraInfo:", e)
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
