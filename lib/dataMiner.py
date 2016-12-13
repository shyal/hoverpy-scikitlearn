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

    from hnMiner import getHNData
    from redditMiner import getRedditData

    getter = {'hn': getHNData, 'reddit': getRedditData}

    for i in range(len(subs)):
        subTitles = getter[subs[i][0]](
            sub=subs[i][1])
        titles += subTitles
        target += [i] * len(subTitles)

    return (titles, target)

if __name__ == "__main__":
    doMining()