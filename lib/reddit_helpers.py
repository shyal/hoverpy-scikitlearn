import requests
import hoverpy
import time
import os


def getRedditComments(args, capture, sub, id):

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

            if args.verbose or capture:
                print("got comment for id %s" % id)
            return extractComments(comments)
        else:
            if args.verbose or capture:
                print "couldn't get comment thread %s" % id
                time.sleep(1)
            else:
                break

    return ""


def getRedditDataByHand(args, limit=100, sub="all"):
    dbpath = "data/reddit.%s.db" % sub
    capture = not os.path.isfile(dbpath)
    with hoverpy.HoverPy(capture=capture,
                         dbpath=dbpath):

        print("getting reddit data for %s" % (sub))

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
                        text += getRedditComments(args,
                                                  capture,
                                                  sub,
                                                  d["data"]["id"])
            else:
                if capture:
                    print(r.json())
                    time.sleep(1)
                else:
                    break

        return titles


import praw


def getRedditData(args, comments=True, limit=100, sub="all"):
    dbpath = "data/reddit.%s.db" % sub
    capture = not os.path.isfile(dbpath)
    with hoverpy.HoverPy(capture=capture,
                         dbpath=dbpath,
                         httpsToHttp=True):
        titles = []
        print "GETTING REDDIT r/%s DATA" % sub
        r = praw.Reddit(user_agent="Karma breakdown 1.0 by /u/_Daimon_",
                        http_proxy="http://localhost:8500",
                        https_proxy="http://localhost:8500",
                        validate_certs="on")
        if not capture:
            r.config.api_request_delay = 0
        subreddit = r.get_subreddit(sub)
        for submission in subreddit.get_hot(limit=limit):
            text = submission.title.lower()
            if comments:
                flat_comments = praw.helpers.flatten_tree(submission.comments)
                for comment in flat_comments:
                    print(comment)
                    if hasattr(comment, 'body'):
                        text += comment.body + " "
            if args.verbose:
                print text
            titles.append(text)
        print("got %i %s" % (len(titles), sub))
        return titles

if __name__ == "__main__":
    for p in getRedditDataPraw(comments=True, sub="technology"):
        print p
