Buliding a Python  social media classifier using a GoLang Service Virtualiser.
==============================================================================

(consider: bringing data mining to the 21st century. Can hoverfly be a tool that aids data mining?)

.. toctree::
   :maxdepth: 2


Virtualising Dependencies
-------------------------

Let's get going:

.. code-block:: bash

    pip install hoverpy
    python

Let's get the top 100 posts on HackerNews

.. literalinclude:: code/hn_titles.py
   :language: python

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

Time taken: **0.196227 seconds**. That's a lot better!


Data mining and caching
-----------------------

In this example we are going to use Hoverfly to harvest our data, however please remember it also caches POSTS, PUTS etc. as well as all for mutating responses via middleware. In fact I could have used it with libraries like Praw or Haxor, but I decided to hit the endpoints directly for efficiency.




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

And finally our ``predict`` function, which takes an array of sentences.

.. literalinclude:: ../../social_media.py
   :language: python
   :lines: 42-49

We can now run our example sentences, and go into our main prediction loop.

.. literalinclude:: ../../social_media.py
   :language: python
   :lines: 53-75

Other use cases
---------------

Indulge me, dear reader, with this thought expriment. Imagine a whole department of developers standing up at once, glancing at each other, and walking away for an "extended lunch-break" while the department next door desperately scrambles to get the culprit service back up.

You suddenly realise it's not only you who can no longer work: no one can. Little by little, chaos sets in: people start wondering around, talking about their weekends, playing table football, throwing things around. This is the corporate equivalent to a big money bonfire.

Now here comes the thought expement: what could you have done, as an engineer, to prevent this all to common situation?

You are affected, but the problem wasn't you
--------------------------------------------

One technique to avoid these "real world" unpredictabilities is mocking. And I'm not using quotes around "real world" to pretend that I know better than people who don't. I'm using them as sometimes one has to stand in awe at the gradual decay of the internet, and how we put up with it.

How many of your bookmarks no longer work? URLs fade into the darkness, and along with them your data. The issue with mocking however is that it tests your code against expected data. What happens when the network gets slow, is wrong, or fails entirely?

To solve this issue I recently wrote a python binding to a wonderful Service Virtualisation application called HoverFly. HoverFly is an ultra-fast light-weight proxy written in GoLang. Using it was a true eye-opener for me, as I can now completely isolate myself from the big nasty and unpredictable world, while pretending its still there.

On my search for dependencies for this blog post, I thought what better than using Hacker News and Reddit. Hacker News is hosted on firebase, which has no rate limit and is actually quite fast. Getting data from Reddit however is a completely different story all together. The rate limit is very low, making it the perfect dependency one cannot depend upon.
