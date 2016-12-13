from lib.parseArgs import args

subs = [('hn', 'showstories'),
        ('hn', 'askstories'),
        ('hn', 'jobstories'),
        ('reddit', 'republican'),
        ('reddit', 'democrat'),
        ('reddit', 'linux'),
        ('reddit', 'music'),
        ('reddit', 'movies'),
        ('reddit', 'literature'),
        ('reddit', 'books')]

titles = []
target = []

from lib.hn_helpers import getHNData
from lib.reddit_helpers import getRedditData

getter = {'hn': getHNData, 'reddit': getRedditData}

for i in range(len(subs)):
    subTitles = getter[subs[i][0]](
        sub=subs[i][1],
        args=args)
    titles += subTitles
    target += [i] * len(subTitles)

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

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

print "*"*30+"\nTEST CLASSIFIER\n"+"*"*30

tests = [
    "powershell and openssl compatability testing",
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
    "dostoevsky's existentialism"
]

predict(tests)

while True:
    predict([raw_input("Enter title: ").strip()])
