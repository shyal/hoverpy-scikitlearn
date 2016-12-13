import unittest

from lib import hnMiner


class test_hn(unittest.TestCase):

    def test_ask(self):
        stories = hnMiner.getHNData(sub="jobstories")
        for story in stories:
            if "hiring" in story:
                self.assertTrue(True)
                return
        self.assertTrue(False)

    def test_show(self):
        stories = hnMiner.getHNData(sub="showstories")
        for story in stories:
            if "show" in story:
                self.assertTrue(True)
                return
        self.assertTrue(False)

    def test_show(self):
        stories = hnMiner.getHNData(sub="askstories")
        for story in stories:
            if "ask" in story:
                self.assertTrue(True)
                return
        self.assertTrue(False)

from lib import redditMiner


class test_reddit(unittest.TestCase):

    def generic_sub_tester(self, sub):
        stories = redditMiner.getRedditData(sub=sub)
        for story in stories:
            if sub in story:
                return True

    def test_linux(self):
        self.assertTrue(self.generic_sub_tester("linux"))

    def test_linux(self):
        self.assertTrue(self.generic_sub_tester("python"))

    def test_music(self):
        self.assertTrue(self.generic_sub_tester("music"))


class test_classifier(unittest.TestCase):

    def test_classifier(self):
        from lib import dataMiner

        titles, target = dataMiner.doMining()

        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.feature_extraction.text import TfidfTransformer
        from sklearn.naive_bayes import MultinomialNB

        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(titles)

        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

        clf = MultinomialNB().fit(X_train_tfidf, target)

        def predict(sentences, answers):
            X_new_counts = count_vect.transform(sentences)
            X_new_tfidf = tfidf_transformer.transform(X_new_counts)

            predicted = clf.predict(X_new_tfidf)

            for doc, category, answer in zip(sentences, predicted, answers):
                print('%r => %s' % (doc, dataMiner.subs[category]))
                self.assertEquals(dataMiner.subs[category], answer)

        print "*"*30+"\nTEST CLASSIFIER\n"+"*"*30

        tests = [
            "powershell and openssl compatability testing",
            "compiling source code on ubuntu",
            "wifi drivers keep crashing",
            "training day was a great movie with a legendary director"
        ]

        answers = [
            ("reddit", "linux"),
            ("reddit", "linux"),
            ("reddit", "linux"),
            ("reddit", "movies"),
        ]

        predict(tests, answers)

if __name__ == "__main__":
    unittest.main()
