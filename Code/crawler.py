#!/usr/bin/env python3


import logging
import sys
import urllib.request as urllib2
import urllib
import lxml
import nltk
import re
import os, os.path
from lxml import html
from bs4 import BeautifulSoup
from queue import *
import numpy as np
from threading import Thread

logger = logging.getLogger(__name__)


class CrawlWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            url, depth = self.queue.get()
            crawl(url, depth)
            self.queue.task_done()


links = []
urlSet=set()

# function that crawls through all the links that come from the seed-link
def crawl(url, depth=3):
    #keeps only the pages, excludes all the pdf, zip, mailto etc.
    try:
        page = urllib2.urlopen(url)
    except (urllib2.URLError, ValueError):
        return None
    if url not in urlSet:
        urlSet.add(url)
        html = page.read()
        dom = lxml.html.fromstring(html)
        root = {}
        root["children"] = []
        root["url"] = url
        root["content"] = html
        download_link(DIR, url, html)
        if depth-1 != 0:
            for link in dom.xpath('//a/@href'):
                queue.put((link, depth - 1))
                try:
                    page = urllib2.urlopen(link)
                except (urllib2.URLError, ValueError):
                    page= None
                if(page is not None)and(link not in root["children"]):
                    root["children"].append(link)
        links.append(root)


def download_link(DIR, url, html):
    # get the soup info of the html
    bsObj = BeautifulSoup(html, "lxml")
    for script in bsObj(["script", "style"]):
        script.extract()
    # set te document ID
    docId = 0
    for file in os.listdir(DIR):
        docId += 1

    # Clear the content of the page to save it in the file
    raw = bsObj.get_text()
    raw = " ".join(raw.split())
    raw = url + '\n' + raw  # add the url in the start of the file
    # save the info in a file
    f = open(DIR + str(docId) + '_idURL.txt', 'w')
    f.write(raw.encode('ascii', 'ignore').decode('ascii'))
    f.close()



# The start of the Script
DIR=sys.argv[2]+"uploads/"
path=sys.argv[2]
try:
    urlSet = np.load(path+'crawlSet.npy').item()
except IOError:
    urlSet=set()
queue = Queue()
# Create 8 worker threads
for x in range(100):
    worker = CrawlWorker(queue)
    # Setting daemon to True will let the main thread exit even though the workers are blocking
    worker.daemon = True
    worker.start()
crawl(sys.argv[1], depth=2)
queue.join()
if not links: #if there is something new
    print ("No need to create new files")
else:
    if os.path.exists(path+'crawlURLrelations.npy'):
        o = np.load(path + 'crawlURLrelations.npy').item()
        for y in o["links"]:
            links.append(y)
    d={}
    d["links"]=links
    np.save(path+'crawlURLrelations.npy', d)
    np.save(path+'crawlSet.npy', urlSet)