import requests
import time


def getHNItem(prot, item, args):
    url = "%s://hacker-news.firebaseio.com/v0/item/%i.json" % (prot, item)
    r = requests.get(url)
    text = ""
    if r.status_code == 200:
        j = r.json()
        if j:
            if "title" in j:
                title = j["title"].lower()
                if args.verbose:
                    print("got url %s" % url)
                    print(title)
                text = title
            if args.text and j.type in ["story", "comment"] and "text" in j:
                post_text = j["text"].lower()
                if args.verbose:
                    print("got url %s" % url)
                    print(post_text)
                text += post_text
            if args.comments and "kids" in j:
                kids = j["kids"]
                for kid in kids:
                    text += getHNItem(prot, kid, args.verbose)
    return text


def getHNData(sub, args):
    print("getting hn %s - this may take a while!" % sub)
    prot = "https" if args.capture else "http"
    start = time.time()
    stories = requests.get(
        "%s://hacker-news.firebaseio.com/v0/%s.json" % (prot, sub)).json()
    titles = []
    for story in stories[:200]:
        titles.append(getHNItem(prot, story, args))

    end = time.time() - start
    print("got %i titles in %f seconds" % (len(titles), end))

    return titles

if __name__ == "__main__":
    getHNData("topstories", True, True)
