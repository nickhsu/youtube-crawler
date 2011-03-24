#!/usr/bin/env python3

import json
import sys

if __name__ == '__main__':
	for line in sys.stdin:
		#line = line.strip()
		try:
			entry = json.loads(line)
			print("{}".format(entry['entry']['id']['$t'].split('/')[-1]))
		except:
			pass
