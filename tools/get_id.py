#!/usr/bin/env python3

import json
import sys

def GAIS_format(entry):
    gais_rec = ''
    gais_rec += "{}".format(entry['entry']['id']['$t'].split('/')[-1])
    return gais_rec

if __name__ == '__main__':
    for line in sys.stdin:
        entry = json.loads(line)
        print(GAIS_format(entry))
