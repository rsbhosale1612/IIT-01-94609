import requests

try:
        url = "https://nilesh-g.github.io/learn-web/data/novels.json"
        responce = requests.get(url)
        print("status code :", responce.status_code)
        data = responce.json()
        print("resp data ",data)

except:
        print("Some error")
