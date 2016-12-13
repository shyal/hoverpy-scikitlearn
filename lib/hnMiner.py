import time
import hoverpy
import os

from hackernews import HackerNews


def getHNData(verbose=False, limit=100, sub="showstories"):
    dbpath = "data/hn.%s.db" % sub
    capture = not os.path.isfile(dbpath)

    with hoverpy.HoverPy(capture=capture, dbpath=dbpath, httpsToHttp=True):
        hn = HackerNews()
        titles = []
        print("GETTING HACKERNEWS %s DATA" % sub)
        subs = {"showstories": hn.show_stories,
                "askstories": hn.ask_stories,
                "jobstories": hn.job_stories}
        for story_id in subs[sub](limit=limit):
            story = hn.get_item(story_id)
            if verbose:
                print(story.title.lower())
            titles.append(story.title.lower())
        print("got %i hackernews titles" % len(titles))
        return titles


if __name__ == "__main__":
    getHNData("topstories", True, True)
