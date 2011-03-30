#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
TODO:
	1. resuce number of threads
	2. using nonblocking I/O for putting entries to server(maybe using a new thread)
'''

import sys
import logging
import httplib2
import time
import threading
import json
import math
import urllib.parse
import getopt

import youtube

DEFAULT_NUM_THREAD = 20
DEFAULT_SERVER_URI = 'http://localhost:4567/'
DEFAULT_NUM_ID_FETCHED = 5000

level = logging.DEBUG
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=level, format=format)

def chunks(l, n):
	#Yield successive n-sized chunks from l.
	for i in range(0, len(l), n):
		yield l[i:i+n]

class YoutubeCrawler:
	class FetcherThread(threading.Thread):
		def __init__(self, vids, entrys, lock):
			self.vids = vids
			self.entrys = entrys
			self.lock = lock
			threading.Thread.__init__(self)

		def run(self):
			fetcher = youtube.Fetcher()
			entrys = []
			for vid in self.vids:
				try:
					#logging.info("get data id = {} in thread {}".format(vid, self.name))
					data = fetcher.get_enrty(vid)
					if data:
						entrys.append(data)
				except IOError:
					fetcher = youtube.Fetcher()
					time.sleep(300)

			self.lock.acquire()
			self.entrys.extend(entrys)
			self.lock.release()

	def __init__(self, num_thread, num_id_fetched, server_uri):
		self.num_id_fetched = num_id_fetched
		self.server_uri = server_uri
		self.num_thread = num_thread
		self.server_conn = httplib2.Http()

	def get_vids(self):
		resp, content = self.server_conn.request("{}/youtube/ids/?limit={}".format(self.server_uri, self.num_id_fetched))
		if resp.status == 200:
			return json.loads(content.decode("utf-8"))
		else:
			return []

	def post_vids(self, vids):
		logging.info("post vids, size = {}".format(len(vids)))
		conn = httplib2.Http()
		data = {'ids': json.dumps(vids)}
		resp, content = conn.request("{}/youtube/fetched_ids/".format(self.server_uri), "POST", urllib.parse.urlencode(data))

	def post_entrys(self, entrys):
		logging.info("post entrys, size = {}".format(len(entrys)))
		conn = httplib2.Http()
		json_data = json.dumps(entrys).encode('utf-8')
		data = {'entrys': json_data}
		while True:
			try:
				resp, content = conn.request("{}/youtube/entrys/".format(self.server_uri), "POST", urllib.parse.urlencode(data))
				break
			except:
				conn = httplib2.Http()

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

			t = threading.Thread(target=self.post_entrys, args=(entrys,))
			t.start()

			t = threading.Thread(target=self.post_vids, args=(vids,))
			t.start()

def usage():
	print("usage: ./client.py -t num_thread -n num_id_fetched -s server_uri")

if __name__ == '__main__':
	try:
		opts, args = getopt.getopt(sys.argv[1:], "t:n:s:h")
	except getopt.GetoptError as err:
		print(err)
		usage()
		sys.exit(2)
	
	num_thread = DEFAULT_NUM_THREAD
	server_uri = DEFAULT_SERVER_URI
	num_id_fetched = DEFAULT_NUM_ID_FETCHED
	for o, a in opts:
		if o == "-t":
			num_thread = int(a)
		elif o == "-n":
			num_id_fetched = int(a)
		elif o == "-s":
			server_uri = "http://{}".format(a)
		elif o == "-h":
			usage()		
	
	crawler = YoutubeCrawler(num_thread, num_id_fetched, server_uri)
	crawler.run()
