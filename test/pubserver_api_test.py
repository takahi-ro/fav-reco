import requests

author = "太宰治"
limit = 10

api_url = "http://pubserver2.herokuapp.com/api/v0.1/books?author={}&limit={}".format(author, limit)
results = requests.get(api_url).json()

print("author:", author)
print("-----------------")
for book_info in results:
    print("title:", book_info["title"])
    print("text_url:", book_info["text_url"])
    print("-----------------")

