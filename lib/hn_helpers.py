from hackernews import HackerNews


def getHNData(comments=False, limit=100, verbose=False):
    hn = HackerNews()
    titles = []
    print "GETTING HACKERNEWS DATA"
    for story_id in hn.top_stories(limit=limit):
        story = hn.get_item(story_id)
        if verbose:
            print(story.title.lower())
        titles.append(story.title.lower())
    print("got %i hackernews titles" % len(titles))
    return titles
