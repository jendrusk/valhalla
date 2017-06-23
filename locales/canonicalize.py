#!/usr/bin/env python
import json
import sys
from collections import OrderedDict

#if its a number sort by the number, if its one of the top level ones use that
#its tags if its parent isnt a number or a top listed one
#otherwise its an instruction so just sort those alphabetically
order = ['posix_locale', 'aliases', 'instructions', 'phrases','SPOT_FOR_TAGS','example_phrases']
def sort_order(parent, k):
  try:
    return int(k)
  except:
    try:
      return order.index(k)
    except:
      pass
  return order.index('SPOT_FOR_TAGS') if parent and not parent.isdigit() and parent not in order else k

#recursively turn a dict into an ordered dict (where insert order is preserved)
#and while doing so sort each subdict using the sorter above
def sort_dict(parent, d):
  ordered = OrderedDict()
  for k, v in sorted(d.iteritems(), key = lambda(k, v): sort_order(parent, k)):
    if isinstance(v, dict):
      ordered[k] = sort_dict(k, v)
    else:
      ordered[k] = v
  return ordered

#open the original file and sort it
with open(sys.argv[1], 'r') as f:
  lang = sort_dict(None, json.load(f))

#format it and write it back out
with open(sys.argv[1], 'w') as f:
  json.dump(lang, f, indent=2)
