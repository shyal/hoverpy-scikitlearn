import hoverpy
import os
import time
import requests
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--capture",
    help="capture the data from hackernews",
    action="store_true")

args = parser.parse_args()

start = time.time()
with hoverpy.HoverPy(capture=args.capture):
    prot = "https" if args.capture else "http"
    r = requests.get(
        "%s://hacker-news.firebaseio.com/v0/topstories.json" % prot)
    for item in r.json()[:100]:
        it = requests.get(
            "%s://hacker-news.firebaseio.com/v0/item/%i.json" % (prot, item))
        print(it.json()["title"])

print("time taken: %f seconds" % (time.time() - start))
