import requests

title = "人間失格"
author = "太宰治"

api_url = "http://pubserver2.herokuapp.com/api/v0.1/books"
params = {
        "title": title,
        "author": author,
        }
results = requests.get(api_url, params).json()


print(results)
print("title:", title)
print("-----------------")
for book_info in results:
    print("title:", book_info["title"])
    print("author:", book_info["authors"][0]["full_name"])
    print("base_book_1:", book_info["base_book_1"])
    print("publisher:", book_info["base_book_1_publisher"])
    print("published at:", book_info["base_book_1_1st_edition"])
    print("text_url:", book_info["text_url"])
    print("-----------------")
