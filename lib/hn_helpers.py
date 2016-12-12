from hackernews import HackerNews
import requests
import time


def getHNData(sub, capture, verbose):
    print("getting hn %s - this may take a while!" % sub)
    prot = "https" if capture else "http"
    start = time.time()
    stories = requests.get(
        "%s://hacker-news.firebaseio.com/v0/%s.json" % (prot, sub)).json()
    titles = []
    for story in stories[:200]:
        url = "%s://hacker-news.firebaseio.com/v0/item/%i.json" % (prot, story)
        r = requests.get(url)

        print json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': '))

        title = r.json()["title"].lower()
        if verbose:
            print("getting url %s" % url)
            print(title)
        titles.append(title)

    end = time.time() - start
    print("got %i titles in %f seconds" % (len(titles), end))

    return titles
