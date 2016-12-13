import hoverpy
import time
import os
import praw


def getRedditData(verbose=False, comments=True, limit=100, sub="all"):
    dbpath = "data/reddit.%s.db" % sub
    capture = not os.path.isfile(dbpath)
    with hoverpy.HoverPy(capture=capture,
                         dbpath=dbpath,
                         httpsToHttp=True) as hp:
        titles = []
        print "GETTING REDDIT r/%s DATA" % sub
        r = praw.Reddit(user_agent="Karma breakdown 1.0 by /u/_Daimon_",
                        http_proxy=hp.httpProxy(),
                        https_proxy=hp.httpProxy(),
                        validate_certs="on")
        if not capture:
            r.config.api_request_delay = 0
        subreddit = r.get_subreddit(sub)
        for submission in subreddit.get_hot(limit=limit):
            text = submission.title.lower()
            if comments:
                flat_comments = praw.helpers.flatten_tree(submission.comments)
                for comment in flat_comments:
                    if hasattr(comment, 'body'):
                        text += comment.body + " "
            if verbose:
                print text
            titles.append(text)
        print("got %i %s" % (len(titles), sub))
        return titles

if __name__ == "__main__":
    for p in getRedditDataPraw(comments=True, sub="technology"):
        print p
