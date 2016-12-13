Speeding up Machine Learning using a high-performance Go proxy.
===============================================================

.. toctree::
   :maxdepth: 2

At times I want to grab a bunch of data, use it, and spit something out the other end. From time to time I get paid to do this, too. But the world of online dependencies is far less predictable than I'd like it to be, a quick browse of your own bookmarks should confirm this to you. Anything that can add predictability to my workflow is surely something worth investing in, and incorporating into my toolset.

.. figure:: hat.jpg
   :alt: hat

Well I recently came across an ultra-high-performance proxy, written in Go, called `HoverFly <http://www.hoverfly.io/>`_. So I decided to write a light-weight Python binding to it: `HoverPy <http://www.hoverpy.io/>`_. HoverFly enables me to offline any data I want, while still being able to interact with it as if I were hitting the real endpoint. In this short article, I'll take you through using this very thin Python layer to build a classifier using scikit-learn, with HackerNews and Reddit as its endpoints.

What I really, really like about Hoverfly, is that it loads so fast in the background. Working with it feels completely transparent, requires zero configuration, and as you'll see I can include its data in my repos; pull that data in for my main functionality, and for my unit testing too. This makes my work 100% water-tight, blazingly fast, and **utterly failure proof**.

Let's begin by cloning the only repo we'll need for this post:

.. code-block:: bash

    git clone https://github.com/shyal/hoverpy-scikitlearn.git
    cd hoverpy-scikilearn
    virtualenv .venv
    source .venv/bin/activate.sh
    pip install -i https://testpypi.python.org/pypi hoverpy
    pip install haxor praw

Data mining HackerNews and Reddit
---------------------------------

.. ./lib/hnMiner.py
   ~~~~~~~~~~~~~~~~

Now that we have our environment setup, let's delve straight in by getting the top 100 posts on HackerNews. To do so, feel free to spin up your ``python`` shell and paste this in, or pass it to the python interpreter with ``python lib/hnMiner.py``

.. literalinclude:: ../../lib/hnMiner.py
   :language: python

Output:

.. code-block:: bash

    got 100 hackernews titles in 14.678717 seconds

You may notice a bolt database was created inside the ``./data`` directory:

.. code-block:: bash

    ll data/hn.topstories.db
    -rw-------  1 ioloop  staff  262144 Dec 13 15:27 data/hn.topstories.db

Let's run the same command again:

.. code-block:: bash

    python lib/hnMiner.py

Output:

.. code-block:: bash

    got 100 hackernews titles in 0.180554 seconds


This is roughly an **80x speedup**, *hitting our endpoint is starting to feel more like hitting a database* which is probably the key point to this chapter.

Note regarding reddit: we can do the same with `lib/redditMiner.py <https://raw.githubusercontent.com/shyal/hoverpy-scikitlearn/master/lib/redditMiner.py>`_: ``python lib/redditMiner.py``. But I think you got the picture.

------------

Putting our miners together
---------------------------

Let's go ahead and write a ``doMining`` function that'll bring in all the data we need from the HN sections, and Reddit subs. You'll need to run this file directly, as it's in the ``./lib`` folder, unless you want to sit around while all the data re-downloads (you don't).

.. literalinclude:: ../../lib/dataMiner.py
   :language: python

command:

.. code-block:: bash

    python lib/dataMiner.py

That's really all we need, and thanks to HoverFly the entire process, once cached, is blazingly fast. Let's move on to our next step.

Building an HN or Reddit classifier
-----------------------------------


Well now that we can transparently cache our dependencies, let's build something interesting. We are going to build a classifier that predicts whether text may have come from HN or Reddit, and also specifically which sub.


.. code-block:: bash

    $ python social_media.py

This spins up our classifier:

.. raw:: html
    
    <script type="text/javascript" src="https://asciinema.org/a/626zkc3hduwfd7328aqme4wgl.js" id="asciicast-626zkc3hduwfd7328aqme4wgl" async></script>

This is our whole classifier, and application entry point, ``./social_media.py``:


.. literalinclude:: ../../social_media.py
   :language: python

Let's break it down a little.

Scikit-learn has a high level component ``CountVectorizer`` that takes care of text preprocessing, tokenizing and filtering of stopwords for us. It transforms our text into feature vectors, in the form of a dictionary:

.. literalinclude:: ../../social_media.py
   :language: python
   :lines: 9-10

You can check the score for various tokens, i.e.

.. code-block:: python

    count_vect.vocabulary_.get(u"python")

The word python appears a total of 21567 in this corpus.

We need to build a tf–idf (term frequency times inverse document frequency) transformer.

.. literalinclude:: ../../social_media.py
   :language: python
   :lines: 12-13

This is to prevent larger documents to score higher, by having occurances score higher due to document size instead of token term relevance, which is why the fix is to divide the term frequencies by the document size.

.. literalinclude:: ../../social_media.py
   :language: python
   :lines: 34-39

And finally our ``predict`` function, which takes an array of sentences.

.. literalinclude:: ../../social_media.py
   :language: python
   :lines: 18-25

-----------------------------------

Taking it one step further with testing
---------------------------------------

At this point I'm hoping you see how water tight this code is. But one is never above unit testing. What is great is that, at this point, since we have zero external data dependencies, the chances of the tests failing are virtually none.

.. literalinclude:: ../../test_social_media.py

In fact we can be so confident about our tests using HoverFly, that we can rest assured our travis tests will most likely never fail. No matter what.

