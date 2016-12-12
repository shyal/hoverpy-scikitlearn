from hackernews import HackerNews
import requests
import time
import json


def getHNItem(prot, item, verbose):
    url = "%s://hacker-news.firebaseio.com/v0/item/%i.json" % (prot, item)
    r = requests.get(url)
    j = r.json()
    if "title" in j:
        title = j["title"].lower()
        if verbose:
            print("getting url %s" % url)
            print(title)
        text = title
    if "kids" in j:
        kids = j["kids"]
        # for kid in kids:

    return text


def getHNData(sub, capture, verbose):
    print("getting hn %s - this may take a while!" % sub)
    prot = "https" if capture else "http"
    start = time.time()
    stories = requests.get(
        "%s://hacker-news.firebaseio.com/v0/%s.json" % (prot, sub)).json()
    titles = []
    for story in stories[:200]:
        titles.append(getHNItem(prot, story, verbose))

    end = time.time() - start
    print("got %i titles in %f seconds" % (len(titles), end))

    return titles


# print json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ':
# '))
