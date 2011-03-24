#!/usr/bin/env python3

import sys
import httplib2
import time
import json
import urllib

SERVER_URL = 'http://gaisq.cs.ccu.edu.tw:4567'

class YoutubeRelatedFetcher:
	def __init__(self):
		self.conn = httplib2.Http()

	def get_related_id(self, vid):
		while True:
			try:
				res, content = self.conn.request("http://gdata.youtube.com/feeds/api/videos/" + vid + "/related?max-results=50&fields=entry(id)&alt=json")
				content = content.decode('utf-8')
				break
			except:
				self.conn = httplib2.Http()
		
		if res.status != 200:
			if content.find("too_many_recent_calls") != -1:
				#ban by server or no video
				raise IOError
			else:
				return False
		else:
			data = json.loads(content)
			related_id = []
			for t in data['feed']['entry']:
				related_id.append(t['id']['$t'].split('/')[-1])
			return related_id

def get_vids():
	conn = httplib2.Http()
	resp, content = conn.request("{}/youtube/related_ids/?limit={}".format(SERVER_URL, 100))
	if resp.status == 200:
		return json.loads(content.decode("utf-8"))
	else:
		return []

def post_vids(vids):
	print("post vids, size = {}".format(len(vids)))
	conn = httplib2.Http()
	data = {'ids': json.dumps(vids)}
	resp, content = conn.request("{}/youtube/ids/".format(SERVER_URL), "POST", urllib.parse.urlencode(data))

def post_vids_fetched(vids):
	print("post vids fetched, size = {}".format(len(vids)))
	conn = httplib2.Http()
	data = {'ids': json.dumps(vids)}
	resp, content = conn.request("{}/youtube/related_ids/".format(SERVER_URL), "POST", urllib.parse.urlencode(data))

if __name__ == '__main__':
	fetcher = YoutubeRelatedFetcher()
	while True:
		vids = get_vids()
		if len(vids) == 0:
			break
		related_ids = []
		for vid in vids:
			try:
				tmp = fetcher.get_related_id(vid)
			except:
				print("sleep")
				time.sleep(300)
			if tmp:
				related_ids.extend(tmp)

		post_vids(related_ids)
		post_vids_fetched(vids)
