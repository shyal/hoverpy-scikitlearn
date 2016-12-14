import time
import vcr
import requests

with vcr.use_cassette('hn.yaml'):
    start = time.time()
    r = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json")
    for item in r.json():
        print(
            requests.get(
                "https://hacker-news.firebaseio.com/v0/item/%i.json" %
                item).json()["title"])
    print("got articles in %f seconds" % (time.time() - start))
