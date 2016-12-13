import requests
import time
import hoverpy
import os


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
            if args.comments and j["type"] in [
                    "story", "comment"] and "text" in j:
                post_text = j["text"].lower()
                if args.verbose:
                    print("got url %s" % url)
                    print(post_text)
                text += post_text
            if args.comments and "kids" in j:
                kids = j["kids"]
                for kid in kids:
                    text += getHNItem(prot, kid, args)
    return text


def getHNDataComments(sub, args):
    hp = hoverpy.HoverPy(capture=args.capture, dbpath=("data/hn.%s.db" % sub))
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

from hackernews import HackerNews


def getHNData(args, comments=False, limit=100, sub="showstories"):
    dbpath = "data/hn.%s.db" % sub
    capture = not os.path.isfile(dbpath)

    with hoverpy.HoverPy(capture=capture, dbpath=dbpath, httpsToHttp=True):
        hn = HackerNews()
        titles = []
        print "GETTING HACKERNEWS DATA"
        subs = {"showstories": hn.show_stories,
                "askstories": hn.ask_stories,
                "jobstories": hn.job_stories}
        for story_id in subs[sub](limit=limit):
            story = hn.get_item(story_id)
            if args.verbose:
                print(story.title.lower())
            titles.append(story.title.lower())
        print("got %i hackernews titles" % len(titles))
        return titles


if __name__ == "__main__":
    getHNData("topstories", True, True)
