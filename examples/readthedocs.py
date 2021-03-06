import time
import hoverpy
import requests

rtd = "http://readthedocs.org/api/v1/project/?limit=50&offset=0&format=json"

with hoverpy.HoverPy(recordMode='once'):
    start = time.time()
    objects = requests.get(rtd).json()['objects']
    links = ["http://readthedocs.org" + x['resource_uri'] for x in objects]
    for link in links:
        response = requests.get(link)
        print("url: %s, status code: %s" % (link, response.status_code))
    print("Time taken: %f" % (time.time() - start))
