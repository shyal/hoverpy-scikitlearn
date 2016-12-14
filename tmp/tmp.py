import time
import hoverpy
import requests
import os

import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

prot = "http" if os.path.isfile("requests.db") else "https"

hp = hoverpy.HoverPy(recordMode='once')

start = time.time()
r = requests.get(
    "%s://hacker-news.firebaseio.com/v0/topstories.json" % (prot))
titles = []
for item in r.json():
    url = "%s://hacker-news.firebaseio.com/v0/item/%i.json" % (prot, item)
    j = requests.get(url).json()
    age = int((time.time()-j["time"])/3600.0)
    # print(age, j["score"], j["title"])
    titles.append(j["title"].lower())
print("got articles in %f seconds" % (time.time() - start))

# print titles

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(titles)

print(count_vect.vocabulary_.get(u"android"))

for key, value in sorted(
        count_vect.vocabulary_.iteritems(), key=lambda k_v: (k_v[1], k_v[0])):
    print "%s: %s" % (key, value)
