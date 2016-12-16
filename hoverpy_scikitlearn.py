def getHNData(verbose=False, limit=100, sub="showstories"):
    from hackernews import HackerNews
    from hackernews import settings
    import hoverpy, time, os

    dbpath = "data/hn.%s.db" % sub
    with hoverpy.HoverPy(recordMode="once", dbpath=dbpath) as hp:
        if not hp.mode() == "capture":
            settings.supported_api_versions[
                "v0"] = "http://hacker-news.firebaseio.com/v0/"
        hn = HackerNews()
        titles = []
        print("GETTING HACKERNEWS %s DATA" % sub)
        subs = {"showstories": hn.show_stories,
                "askstories": hn.ask_stories,
                "jobstories": hn.job_stories,
                "topstories": hn.top_stories}
        start = time.time()
        for story_id in subs[sub](limit=limit):
            story = hn.get_item(story_id)
            if verbose:
                print(story.title.lower())
            titles.append(story.title.lower())
        print(
            "got %i hackernews titles in %f seconds" %
            (len(titles), time.time() - start))
        return titles

def getRedditData(verbose=False, comments=True, limit=100, sub="all"):
    import hoverpy, praw, time
    dbpath = ("data/reddit.%s.db" % sub)
    with hoverpy.HoverPy(recordMode='once', dbpath=dbpath, httpsToHttp=True) as hp:
        titles = []
        print "GETTING REDDIT r/%s DATA" % sub
        r = praw.Reddit(user_agent="Karma breakdown 1.0 by /u/_Daimon_", http_proxy=hp.httpProxy(), https_proxy=hp.httpProxy(), validate_certs="off")
        if not hp.mode() == "capture":
            r.config.api_request_delay = 0
        subreddit = r.get_subreddit(sub)
        for submission in subreddit.get_hot(limit=limit):
            text = submission.title.lower()
            if comments:
                flat_comments = praw.helpers.flatten_tree(submission.comments)
                for comment in flat_comments:
                    text += comment.body + " " if hasattr(comment, 'body') else ''
            if verbose:
                print text
            titles.append(text)
        return titles

subs = [('hn', 'showstories'),
        ('hn', 'askstories'),
        ('hn', 'jobstories'),
        ('reddit', 'republican'),
        ('reddit', 'democrat'),
        ('reddit', 'linux'),
        ('reddit', 'python'),
        ('reddit', 'music'),
        ('reddit', 'movies'),
        ('reddit', 'literature'),
        ('reddit', 'books')]

def doMining():
    titles = []
    target = []
    getter = {'hn': getHNData, 'reddit': getRedditData}
    for i in range(len(subs)):
        subTitles = getter[subs[i][0]](
            sub=subs[i][1])
        titles += subTitles
        target += [i] * len(subTitles)
    return (titles, target)

sentences = ["powershell and openssl compatability testing",
    "compiling source code on ubuntu",
    "wifi drivers keep crashing",
    "cron jobs",
    "training day was a great movie with a legendary director",
    "michael bay should remake lord of the rings, set in the future",
    "hilary clinton may win voters' hearts",
    "donald trump may donimate the presidency",
    "reading dead wood gives me far more pleasure than using kindles",
    "hiring a back end engineer",
    "guitar is louder than the piano although electronic is best",
    "drum solo and singer from the rolling stones",
    "hiring a back end engineer",
    "javascript loader",
    "dostoevsky's existentialis"]


def main():
    titles, target = doMining()

    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.naive_bayes import MultinomialNB

    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(titles)

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    clf = MultinomialNB().fit(X_train_tfidf, target)

    print "*"*30+"\nTEST CLASSIFIER\n"+"*"*30

    def predict(sentences):
        X_new_counts = count_vect.transform(sentences)
        X_new_tfidf = tfidf_transformer.transform(X_new_counts)

        predicted = clf.predict(X_new_tfidf)

        for doc, category in zip(sentences, predicted):
            print('%r => %s' % (doc, subs[category]))

    predict(sentences)

    while True:
        predict([raw_input("Enter title: ").strip()])

if __name__ == "__main__":
    main()
