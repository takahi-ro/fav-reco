import requests

url = "https://api.bungomail.com/v0/books"
params = {
        "作品名": "羅生門",
        "limit": 1
        }


result_json = requests.get(url, params).json()
for k, v in result_json.items():
    print(k)
