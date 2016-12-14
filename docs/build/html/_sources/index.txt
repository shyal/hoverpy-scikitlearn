Speeding up scikit-learn workflow using a high-performance Go proxy.
====================================================================

.. toctree::
   :maxdepth: 2

I recently came across an ultra-high-performance GoLang caching proxy, and wanted to see if I could use it to speed-up my scikit-learn based work. Up until now I've been using vcrpy to cache my requests during the mining phase, so I wanted to do a speed comparison.

.. code-block:: bash
  
    pip install hoverpy --user

Example:

.. code-block:: python

    import time
    import hoverpy
    import requests

    start = time.time()

    rtd = "http://readthedocs.org/api/v1/project/?limit=50&offset=0&format=json"

    with hoverpy.HoverPy(recordMode='once'):
        objects = requests.get(rtd).json()['objects']
        links = ["http://readthedocs.org" + x['resource_uri'] for x in objects]
        for link in links:
            response = requests.get(link)
            print("url: %s, status code: %s" % (link, response.status_code))
        print("Time taken: %f" % (time.time() - start))

Ouput:

.. code-block:: bash
    
    [...]
    Time taken: 9.418862

Upon second invocation:

.. code-block:: bash
    
    [...]
    Time taken: 0.093463

That's much better: *100.78x* faster than hitting the real endpoint.

.. figure:: http_diff.png

Not surprising really. My issue with caching proxies however, is that it's the https handshaking that takes time–not fetching the data–and one of my many annoyances with vcrpy is that it won't let me remap https requests to http.

Therefore I was very pleased to see remapping work perfectly in hoverpy (code provided below the next graph). This lead to hoverpy wiping the floor with vcrpy; over 13x faster:

.. figure:: https_get.png

.. literalinclude:: ../../examples/hn.py
   :language: python

I'm very impressed with hoverpy's performance.

Data mining HN
---------------------------------

What I also really like about Hoverfly is how fast it loads, and how fast it loads up the boltdb database. I also like the fact it's configuration-free. Here's a function you can use for all your HN data mining needs:

.. literalinclude:: ../../lib/hnMiner.py
   :language: python


------------

Data mining Reddit
-------------------

While we're at it, let's put a function here for offlining subreddits.

.. literalinclude:: ../../lib/redditMiner.py
    :language: python


Building an HN or Reddit classifier
-----------------------------------

OK time to play. I'm going to build a naive bayesian text classifier. You'll be able to type in some text, and it'll tell you which subreddit it thinks the text could have originated from.

We still have a bit more mining work to do. Let's bring in all the subs and sections we need, and build our data for classification:

.. literalinclude:: ../../lib/dataMiner.py
   :language: python
   :lines: 4-27

That's all our data mining done. I think this is a good time to remind ourselves a big part of machine learning is, in fact, data sanitisation and mining.

-----------------------------------


.. .. raw:: html
    
    <script type="text/javascript" src="https://asciinema.org/a/626zkc3hduwfd7328aqme4wgl.js" id="asciicast-626zkc3hduwfd7328aqme4wgl" async></script>

For this part, you'll need scikit-learn.

.. code-block:: bash

    pip install sklearn numpy scipy

Running the classifier:

.. literalinclude:: ../../social_media.py
   :language: python
   :lines: 3-33

In case you are not familiar with tokenizing, tfidf, classification etc. then I've provided a link at the end of this tutorial that'll demistify the block above.

-----------------------------------


.. image:: https://travis-ci.org/shyal/hoverpy-scikitlearn.svg?branch=master
    :target: https://travis-ci.org/shyal/hoverpy-scikitlearn

http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html