import hoverpy
import praw
import os
import time

sub = "python"
db = ("%s.db" % sub)
capture = not os.path.isfile(db)

with hoverpy.HoverPy(dbpath=db, recordMode='once') as hp:
    start = time.time()
    titles = []
    print "GETTING REDDIT r/%s DATA" % sub
    r = praw.Reddit(user_agent="Karma breakdown 1.0 by /u/_Daimon_",
                    http_proxy=hp.httpProxy(),
                    https_proxy=hp.httpsProxy(),
                    validate_certs="off")
    if not capture:
        r.config.api_request_delay = 0
    subreddit = r.get_subreddit(sub)
    for submission in subreddit.get_hot(limit=100):
        text = submission.title.lower()
        print(text)
        for comment in praw.helpers.flatten_tree(submission.comments):
            if hasattr(comment, 'body'):
                text += comment.body + " "
    titles.append(text)
    print("got %i %s in %f" % (len(titles), sub, time.time() - start))
