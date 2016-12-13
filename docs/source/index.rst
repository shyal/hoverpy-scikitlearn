Speeding up Machine Learning using a high-performance Go proxy.
===============================================================

.. toctree::
   :maxdepth: 2

At times I want to grab a bunch of data, use it, and spit something out the other end. From time to time I get paid to do this, too. But the world of online dependencies is far less predictable than I'd like it to be, a quick browse of your own bookmarks should confirm this to you. Anything that can add predictability to my workflow is surely something worth investigating, and incorporating into my toolset.

Well I recently came across an ultra-high-performance proxy, written in Go, called `HoverFly <http://www.hoverfly.io/>`_. So I decided to write a light-weight Python binding to it: `HoverPy <http://www.hoverpy.io/>`_. HoverFly enables me to offline any data I want, while still being able to interact with it as if I were hitting the real endpoint. In this short article, I'll take you through using this very thin Python layer to build a classifier using SciKitLearn, with HackerNews and Reddit as its endpoints.

What I really, really like about Hoverfly, is that it loads so fast in the background. Working with it feels completely transparent, and as you'll see I can include its data in my repos; pull that data in for my main functionality, and for my unit testing too. This makes my work 100% water-right, blazingly fast, and failure proof.

Data mining HackerNews and Reddit
---------------------------------

Let's get going:

.. code-block:: bash

    pip install hoverpy haxor praw
    python

./lib/hnMiner.py
~~~~~~~~~~~~~~~~~

Let's get the top 100 posts on HackerNews

.. literalinclude:: ../../lib/hnMiner.py
   :language: python

We can do the same with ``lib/redditMiner.py``.


Let's run this, and get the top 100 titles on HN:

.. code-block:: bash
  
    $ ./hn_titles.py --capture
    
    [...]
    London house prices are having a relatively bad December
    Interview with Max Levchin

    time taken: 15.888608 seconds.

Time taken: **15.888608 seconds**. I don't know about you, but working with dependencies that take around 15 seconds on each run is simply not workable. So Let's now see what happens when we run this code in simulate mode.


.. code-block:: bash
  
    $ ./hn_titles.py --capture
    
    [...]
    London house prices are having a relatively bad December
    Interview with Max Levchin

    time taken: 0.196227 seconds.

Time taken: **0.196227 seconds**. That's an 80x speed-up: fast enough to collect a meaningful chunk of data transparently.

Putting our miners together
---------------------------

Let's go ahead and write a ``doMining`` function that'll bring in all the data we need from the HN sections, and Reddit subs.

.. literalinclude:: ../../lib/dataMiner.py
   :language: python

That's really all we need, and thanks to HoverFly the entire process, once cached, is blazingly fast. Let's move on to our next step.

Building an HN or Reddit classifier
-----------------------------------


.. figure:: hat.jpg
   :alt: hat

Well now that we can transparently cache our dependencies, let's build something interesting. We are going to build a classifier that predicts whether text may have come from HN or Reddit, and also specifically which sub.


.. code-block:: bash

    $ python social_media.py

This spins up our classifier:

.. literalinclude:: code/social_media_output.txt

Everything under *TEST CLASSIFIER* is the result of running these strings through the classifier. Let's break this down, and see how it works. Feel free to type in text, and see how the classifier holds up. See whether you can formuate sentences that would fall within the specified subs.

./social_media.py
-----------------

.. literalinclude:: ../../social_media.py
   :language: python
   :lines: 1-13

Scikitlearn has a high level component ``CountVectorizer`` that takes care of text preprocessing, tokenizing and filtering of stopwords for us. It transforms our text into feature vectors, in the form of a dictionary:

.. literalinclude:: ../../social_media.py
   :language: python
   :lines: 29-34

You can check the score for various tokens, i.e.

.. code-block:: python

    count_vect.vocabulary_.get(u"solarcity")

Output: 13350

We need to build a tf–idf (term frequency times inverse document frequency) transformer. This is to prevent larger documents to score higher, by having occurances score higher due to document size instead of token term relevance, which is why the fix is to divide the term frequencies by the document size.

.. literalinclude:: ../../social_media.py
   :language: python
   :lines: 34-39

And finally our ``predict`` function, which takes an array of sentences.

.. literalinclude:: ../../social_media.py
   :language: python
   :lines: 42-49

We can now run our example sentences, and go into our main prediction loop.

.. literalinclude:: ../../social_media.py
   :language: python
   :lines: 53-75

Testing
-------

Indulge me, dear reader, with this thought expriment. Imagine a whole department of developers standing up at once, glancing at each other, and walking away for an "extended lunch-break" while the department next door desperately scrambles to get the culprit service back up.

You suddenly realise it's not only you who can no longer work: no one can. Little by little, chaos sets in: people start wondering around, talking about their weekends, playing table football, throwing things around. This is the corporate equivalent to a big money bonfire.

Now here comes the thought expement: what could you have done, as an engineer, to prevent this all to common situation?

You are affected, but the problem wasn't you
--------------------------------------------

One technique to avoid these "real world" unpredictabilities is mocking. And I'm not using quotes around "real world" to pretend that I know better than people who don't. I'm using them as sometimes one has to stand in awe at the gradual decay of the internet, and how we put up with it.

How many of your bookmarks no longer work? URLs fade into the darkness, and along with them your data. The issue with mocking however is that it tests your code against expected data. What happens when the network gets slow, is wrong, or fails entirely?

To solve this issue I recently wrote a python binding to a wonderful Service Virtualisation application called HoverFly. HoverFly is an ultra-fast light-weight proxy written in GoLang. Using it was a true eye-opener for me, as I can now completely isolate myself from the big nasty and unpredictable world, while pretending its still there.

On my search for dependencies for this blog post, I thought what better than using Hacker News and Reddit. Hacker News is hosted on firebase, which has no rate limit and is actually quite fast. Getting data from Reddit however is a completely different story all together. The rate limit is very low, making it the perfect dependency one cannot depend upon.
