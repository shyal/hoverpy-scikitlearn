Dependable dependencies, and machine learning.
==============================================

.. toctree::
   :maxdepth: 2

Indulge me, dear reader, with this thought expriment. Imagine a whole department of developers standing up at once, glancing at each other, and walking away for an "extended lunch-break" while the department next door desperately scrambles to get the culprit service back up.

.. figure:: 1ftcd5.jpg
   :alt: sometimes the world can be an unpredictable place

You suddenly realise it's not only you who can no longer work: no one can. Little by little, chaos sets in: people start wondering around, talking about their weekends, playing table football, throwing things around. This is the corporate equivalent to a big money bonfire.

You are affected, but the problem wasn't you
--------------------------------------------

One technique to avoid these "real world" unpredictabilities is mocking. And I'm not using quotes around "real world" to pretend that I know better than people who don't. I'm using them as sometimes one has to wonder how this whole internet thing holds together anyway.

How many of your bookmarks no longer work? URLs fade into the darkness, and along with them your data. The issue with mocking however is that it tests your code against expected data. What happens when the network gets slow, data is not what you expected, or the myriad of other things that can go wrong?

Welcome to the world of service virtualisation. To solve this issue I recently wrote a python binding to a wonderful application written in Go, called HoverFly. This was a true eye-opener for me, as I can now completely isolate myself from the big nasty and unpredictable world, while pretending its still there.

On my search for dependencies for this blog post, I thought what better than using Hacker News and Reddit. Hacker News is hosted on firebase, which has no rate limit and is actually quite fast. Getting data from Reddit however is a completely different story all together. The rate limit is very low, making it the perfect dependency one cannot depend upon.

Virtualising Dependencies
-------------------------

Let's get going:

.. code-block:: bash

    pip install hoverpy
    python

Let's get the top 50 posts on HackerNews

.. literalinclude:: code/hn_titles.py
   :language: python

Let's run this, and get the top 100 titles on HN:

.. code-block:: bash
  
    $ ./hn_titles.py --capture
    
    [...]
    London house prices are having a relatively bad December
    Interview with Max Levchin

    time taken: 15.888608 seconds.

Time taken: **15.888608 seconds**. I don't know about you, but working with dependencies that take a while 15 seconds on each run is simply not workable. So Let's now see what happens when we run this code in simulate mode.


.. code-block:: bash
  
    $ ./hn_titles.py --capture
    
    [...]
    London house prices are having a relatively bad December
    Interview with Max Levchin

    time taken: 0.196227 seconds.

Time taken: **0.196227 seconds**. That's a lot better!


Building an HN or Reddit classifier
-----------------------------------


.. figure:: hat.jpg
   :alt: hat

Well now that we can transparently cache our dependencies, let's build something interesting. We are going to build a classifier that predicts whether text may have come from HN or Reddit, and also specifically which sub.


.. code-block:: bash

    $ python social_media.py --comments --text

This spins up our classifier:

.. literalinclude:: code/social_media_output.txt

Everything under *TEST CLASSIFIER* is the result of running these strings through the classifier. Let's break this down, and see how it works. Feel free to type in text, and see how the classifier holds up.


.. literalinclude:: ../../social_media.py
   :language: python
   :lines: 1-13

Above we simply build an array of subs.

Please note, if you are copy and pasting these examples, you'll need to set some args to true here:

.. code-block:: python

    args.comments = True
    args.text = True

Next, we built out getters, and then actually went to fetch the post titles, text, and comments from HN and Reddit.

.. literalinclude:: ../../social_media.py
   :language: python
   :lines: 14-27


Scikitlearn has a high level component that takes care of text preprocessing, tokenizing and filtering of stopwords for us. It transforms our text into feature vectors, in the form of a dictionary:

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
