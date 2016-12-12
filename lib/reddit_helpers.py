import praw


def getRedditData(comments=False, limit=100, verbose=False, sub="all"):
    titles = []
    print "GETTING REDDIT r/%s DATA" % sub
    r = praw.Reddit(user_agent="Karma breakdown 1.0 by /u/_Daimon_",
                    http_proxy="http://localhost:8500",
                    https_proxy="http://localhost:8500",
                    validate_certs="on")
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
