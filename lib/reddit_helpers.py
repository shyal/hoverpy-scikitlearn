import requests
import hoverpy


def getRedditData(args, limit=100, verbose=False, sub="all"):
    hp = hoverpy.HoverPy(capture=args.capture, dbpath="reddit.db")

    print("getting reddit data for %s" % (sub))
    print("*"*50)

    r = requests.get(
        "http://www.reddit.com/r/%s.json?limit=%i" %
        (sub, limit))

    print(r.status_code)

    data = r.json()

    if data and "data" in data:
        data = data["data"]
        text = ""
        for d in data["children"]:
            if "title" in d["data"]:
                title = d["data"]["title"]
                print "title:" + title
                text += title
            if "selftext" in d["data"] and d["data"]["selftext"]:
                selftext = d["data"]["selftext"]
                print "selftext: " + selftext
                text += selftext
        return text

if __name__ == "__main__":
    class Args:

        def __init__(self):
            self.capture = True

    getRedditData(Args(), sub="books")
    getRedditData(Args(), sub="movies")
    getRedditData(Args(), sub="music")
