#!/usr/bin/env python
import sys
import pymongo
import Queue
import threading
import urllib2
import time
import re

NUM_THREAD = 5

def get_vid_list(data):
	return re.findall('<id>http:\/\/gdata.youtube.com\/feeds\/api\/videos\/(.*?)<\/id>', data)

class ThreadFetcher(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):
		global db
		while True:
			vid = self.queue.get()
			url = "http://gdata.youtube.com/feeds/api/videos/" + vid + "/related?max-results=50&fields=entry(id)"
			print("get " + vid)
			try:
				data = urllib2.urlopen(url).read()
				if data == None or data.find("too_many_recent_calls") != -1:
					print("sleep")
					time.sleep(60)
				else:
					for x in get_vid_list(data):
						db['vid'].insert({"id": x})
					db['vid'].update({'id':vid}, {"$set": {"get_related": True}})
			except:
				pass
			self.queue.task_done()


while (True):
	queue = Queue.Queue()

	#start fetcher
	for i in range(NUM_THREAD):
		t = ThreadFetcher(queue)
		t.setDaemon(True)
		t.start()

	#init queue
	for vid in db['vid'].find({'get_related': False}).limit(10000):
		queue.put(vid['id'])

	queue.join()
