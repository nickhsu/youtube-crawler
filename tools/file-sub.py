#!/usr/bin/env python3

import sys

f1 = open(sys.argv[1], "r")
f2 = open(sys.argv[2], "r")

s = set()
for line in f2:
    s.add(line.strip())

for line in f1:
    line = line.strip()
    if line not in s:
        print(line)
