import argparse
from lib.hn_helpers import getHNData
from lib.reddit_helpers import getRedditData

from hoverpy import HoverPy

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
args = parser.parse_args()

hp = HoverPy()

limit = 10

if args.capture:
    hp.capture()
else:
    hp.simulate()

subs = [
    'music',
    'democrats',
    'republicans',
    'movies',
    'books']

titles = []
target = []

for i in range(len(subs)):
    subTitles = getRedditData(
        sub=subs[i],
        verbose=args.verbose,
        comments=True,
        limit=limit)
    titles += subTitles
    target += [i] * len(subTitles)

hnTitles = getHNData(verbose=args.verbose, limit=limit, comments=True)
titles += hnTitles
target += [len(subs)] * len(hnTitles)

categories = subs + ['hackernews']

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
        print('%r => %s' % (doc, categories[category]))

while True:
    predict([raw_input("Enter title: ").strip()])
