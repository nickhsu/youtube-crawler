# -*- coding: utf-8 -*-

import httplib2
import json

class Fetcher:
	def __init__(self, api_key):
		self.__conn = httplib2.Http()
		self.__api_key = api_key

	def get_enrty(self, vid):
		res, content = self.__req("http://gdata.youtube.com/feeds/api/videos/" + vid + "?alt=json&key=" + self.__api_key)
		#print(res)
		#print("\n")
		if res.status != 200:
			#print(res)
			#print("\n")
			#print(content)
			#print("\n")
			#self.__conn = httplib2.Http()
			#logging.debug("status error:{}, {}".format(res.status, content))
			if content.find("too_many_recent_calls") != -1:
				#ban by server or no video
				raise IOError
			else:
				return False
		else:
			return content
	
	def get_related_vid(self, vid):
		res, content = self.__req("http://gdata.youtube.com/feeds/api/videos/" + vid + "/related?max-results=50&fields=entry(id)&alt=json")
		
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

	def __req(self, url):
		while True:
			try:
				res, content = self.__conn.request(url)
				content = content.decode('utf-8')
				break
			except:
				self.__conn = httplib2.Http()
		return res, content
