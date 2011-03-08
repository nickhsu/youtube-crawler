#!/usr/bin/env python3

import json
import sys

def GAIS_format(entry):
    gais_rec = '@\n'
    gais_rec += "@id:{}\n".format(entry['entry']['id']['$t'])
    gais_rec += "@published:{}\n".format(entry['entry']['published']['$t'])
    gais_rec += "@updated:{}\n".format(entry['entry']['updated']['$t'])
    gais_rec += "@title:{}\n".format(entry['entry']['title']['$t'])
    gais_rec += "@author:{}\n".format(entry['entry']['author'][0]['name']['$t'])
    try:
        gais_rec += "@desc:{}\n".format(entry['entry']['content']['$t'])
    except:
        pass
    try:
        gais_rec += "@keywords:{}\n".format(entry['entry']['media$group']['media$keywords']['$t'])
    except:
        pass

    #category
    entry['entry']['category'].pop(0)
    category = ''
    for c in entry['entry']['category']:
        category += "{},".format(c['term'])
    gais_rec += "@category:{}".format(category) #final line doesn't need "\n"
    
    return gais_rec

if __name__ == '__main__':
    for line in sys.stdin:
        entry = json.loads(line)
        print(GAIS_format(entry))
