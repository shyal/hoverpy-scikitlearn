import json
import requests


def getRedditData(comments=False, limit=100, verbose=False, sub="all"):
    data = requests.get("http://www.reddit.com/r/%s.json" % sub).json()
    for d in data["data"]["children"]:
        if "title" in d["data"]:
            print d["data"]["title"]
        if "selftext" in d["data"] and d["data"]["selftext"]:
            print d["data"]["selftext"]

if __name__ == "__main__":
    import hoverpy
    with hoverpy.HoverPy(capture=False) as hp:
        getRedditData()
