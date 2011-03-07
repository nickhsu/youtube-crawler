#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
TODO:
    1. resuce number of threads
    2. using nonblocking I/O for putting entries to server(maybe using a new thread)
'''

import sys
import logging
import subprocess
import httplib2
import time
import tempfile
import threading
import json
import math
import logging
import urllib.parse

NUM_THREAD = 10
SERVER_URI = 'http://gaisq.cs.ccu.edu.tw:4567/'
NUM_ID_FETCHED = 3000

level = logging.DEBUG
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=level, format=format)

def chunks(l, n):
    #Yield successive n-sized chunks from l.
    for i in range(0, len(l), n):
        yield l[i:i+n]

class YoutubeFetcher:
    def __init__(self):
        self.conn = httplib2.Http()

    def get_enrty(self, vid):
        res, content = self.conn.request("http://gdata.youtube.com/feeds/api/videos/" + vid + "?alt=json")
        content = content.decode('utf-8')
        if res.status != 200:
            logging.debug("status error:{}, {}".format(res.status, content))
            if content.find("too_many_recent_calls") != -1:
                #ban by server or no video
                raise IOError
            else:
                return False
        else:
            return content

class YoutubeCrawler:
    class FetcherThread(threading.Thread):
        def __init__(self, vids, entrys, lock):
            self.vids = vids
            self.entrys = entrys
            self.lock = lock
            threading.Thread.__init__(self)

        def run(self):
            fetcher = YoutubeFetcher()
            entrys = []
            for vid in self.vids:
                try:
                    #logging.info("get data id = {} in thread {}".format(vid, self.name))
                    data = fetcher.get_enrty(vid)
                    if data:
                        entrys.append(data)
                except IOError:
                    time.sleep(300)

                self.lock.acquire()
                self.entrys.extend(entrys)
                self.lock.release()

    def __init__(self, num_thread):
        self.num_thread = num_thread
        self.server_conn = httplib2.Http()

    def get_vids(self):
        resp, content = self.server_conn.request("{}youtube/ids/?limit={}".format(SERVER_URI,NUM_ID_FETCHED))
        if resp.status == 200:
            return json.loads(content.decode("utf-8"))
        else:
            return []

    def post_vids(self, vids):
        data = {'ids': json.dumps(vids)}
        resp, content = self.server_conn.request("{}youtube/fetched_ids/".format(SERVER_URI), "POST", urllib.parse.urlencode(data))

    def post_entrys(self, entrys):
        data = {'entrys': json.dumps(entrys)}
        resp, content = self.server_conn.request("{}youtube/entrys/".format(SERVER_URI), "POST", urllib.parse.urlencode(data))

    def run(self):
        while True:
            entrys = []
            threads = []
            lock = threading.Lock()
            vids = self.get_vids()

            if len(vids) == 0:
                break

            for x in chunks(vids, math.ceil(len(vids) / self.num_thread)):
                t = self.FetcherThread(x, entrys, lock)
                t.setDaemon(True)
                threads.append(t)
                t.start()
            for t in threads:	
                t.join()

            self.post_vids(vids)
            self.post_entrys(entrys)

if __name__ == '__main__':
    crawler = YoutubeCrawler(NUM_THREAD)
    crawler.run()
