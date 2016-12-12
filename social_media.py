import argparse
from lib.hn_helpers import getHNData
from lib.reddit_helpers import getRedditData

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

parser = argparse.ArgumentParser()
parser.add_argument(
    "--capture",
    help="capture the data from hackernews",
    action="store_true")
parser.add_argument(
    "--verbose",
    help="print more information",
    action="store_true")
parser.add_argument(
    "--comments",
    help="include comments",
    action="store_true")
parser.add_argument(
    "--text",
    help="include post text",
    action="store_true")
args = parser.parse_args()


def main():

    subs = [('hn', 'showstories'),
            ('hn', 'askstories'),
            ('hn', 'jobstories'),
            ('reddit', 'music'),
            ('reddit', 'movies'),
            ('reddit', 'books')]

    titles = []
    target = []

    for i in range(len(subs)):
        if subs[i][0] == 'hn':
            subTitles = getHNData(
                sub=subs[i][1],
                args=args)
        if subs[i][0] == 'reddit':
            subTitles = getRedditData(
                sub=subs[i][1],
                args=args)
        titles += subTitles
        target += [i] * len(subTitles)

    print target

    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(titles)

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    clf = MultinomialNB().fit(X_train_tfidf, target)

    def predict(sentences):
        X_new_counts = count_vect.transform(sentences)
        X_new_tfidf = tfidf_transformer.transform(X_new_counts)

        predicted = clf.predict(X_new_tfidf)

        for doc, category in zip(sentences, predicted):
            print('%r => %s' % (doc, subs[category]))

    while True:
        predict([raw_input("Enter title: ").strip()])


if __name__ == "__main__":
    main()
    # print getRedditData(
    #     sub="movies",
    #     args=args)
