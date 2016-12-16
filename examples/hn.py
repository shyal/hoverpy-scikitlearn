import time
import hoverpy
import requests
import os

prot = "http" if os.path.isfile("hn.db") else "https"

with hoverpy.HoverPy(recordMode='once', dbpath='hn.db') as hp:
    print("started hoverpy in %s mode" % hp.mode())
    start = time.time()
    r = requests.get(
        "%s://hacker-news.firebaseio.com/v0/topstories.json" % (prot))
    for item in r.json():
        print(
            requests.get(
                "%s://hacker-news.firebaseio.com/v0/item/%i.json" %
                (prot, item)).json()["title"])
    print("got articles in %f seconds" % (time.time() - start))
