import requests
import hoverpy
import time


def getRedditComments(args, sub, id):

    success = False

    while not success:
        r = requests.get(
            "http://www.reddit.com/r/%s/comments/%s.json" % (sub, id))

        success = r.status_code == 200

        if success:
            data = r.json()
            comments = data[1]["data"]["children"]

            def extractComments(comments):

                text = ""

                for comment in comments:
                    if "body" in comment:
                        text += comment["data"]["body"]
                        replies = comment["data"]["replies"]
                        if isinstance(replies, dict):
                            data = replies["data"]
                            text += extractComments(data["children"])

                return text

            print("got comment for id %s" % id)
            return extractComments(comments)
        else:
            if args.capture:
                print "couldn't get comment thread!"
                time.sleep(3)
            else:
                break

    return ""


def getRedditData(args, limit=100, sub="all"):
    with hoverpy.HoverPy(capture=args.capture, dbpath="reddit.db"):

        print("getting reddit data for %s" % (sub))
        print("*"*50)

        success = False
        titles = []

        while not success:
            r = requests.get(
                "http://www.reddit.com/r/%s.json?limit=%i" %
                (sub, limit))

            success = r.status_code == 200
            if success:
                data = r.json()
                if data and "data" in data:
                    data = data["data"]
                    for d in data["children"]:
                        text = ""
                        if "title" in d["data"]:
                            title = d["data"]["title"].lower()
                            text += title
                        if "selftext" in d["data"] and d["data"]["selftext"]:
                            selftext = d["data"]["selftext"].lower()
                            text += selftext
                        titles.append(text)
                        text += getRedditComments(args, sub, d["data"]["id"])
            else:
                if args.capture:
                    print(r.json())
                    time.sleep(1)
                else:
                    break

        return titles

if __name__ == "__main__":
    class Args:

        def __init__(self):
            self.capture = False

    print getRedditData(Args(), sub="books")

    # getRedditData(Args(), sub="movies")
    # getRedditData(Args(), sub="music")
    #
    # with hoverpy.HoverPy(capture=False, dbpath="reddit.db"):
    #     print getRedditComments("books", "5hwj6m")
