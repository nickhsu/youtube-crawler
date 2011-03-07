#!/usr/bin/env python3

import sys

vid_db = open(sys.argv[1], "r")
fetched = open(sys.argv[2], "r")

vids = set()
for line in fetched:
    vids.add(line.strip())

for line in vid_db:
    vid = line.strip()
    if vid not in vids:
        print(vid)
