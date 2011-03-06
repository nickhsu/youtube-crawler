#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
			return False
		if content.find("too_many_recent_calls") != -1:
			#ban by server or no video
			raise IOError
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
					logging.info("get data id = {} in thread {}".format(vid, self.name))
					data = fetcher.get_enrty(vid)
					if data:
						entrys.append(data)
				except IOError:
					time.sleep(60)
			
			self.lock.acquire()
			self.entrys.extend(entrys)
			self.lock.release()

	def __init__(self, num_thread):
		self.num_thread = num_thread
		self.server_conn = httplib2.Http()

	def get_vids(self):
		resp, content = self.server_conn.request("http://localhost:4567/youtube/ids/?limit=100")
		if resp.status == 200:
			return json.loads(content.decode("utf-8"))
		else:
			return []

	def post_vids(self, vids):
		data = {'ids': json.dumps(vids)}
		resp, content = self.server_conn.request("http://localhost:4567/youtube/fetched_ids/", "POST", urllib.parse.urlencode(data))

	def post_entrys(self, entrys):
		data = {'entrys': json.dumps(entrys)}
		resp, content = self.server_conn.request("http://localhost:4567/youtube/entrys/", "POST", urllib.parse.urlencode(data))

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
	crawler = YoutubeCrawler(10)
	crawler.run()
