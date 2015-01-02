########################################################################
#
# File Name:            Set.py
#
#
"""
WWW: http://4suite.org/         e-mail: support@4suite.org

Copyright (c) 2000-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""



def Not(original,other):
    return filter(lambda x,other=other:x not in other,original)

def Union(left,right):
    if len(left) < len(right):
        loop = left
        compare = right
    else:
        loop = right
        compare = left
    return compare + filter(lambda x,compare = compare:x not in compare,loop)

def Intersection(left,right):
    if len(left) < len(right):
        loop = left
        compare = right
    else:
        loop = right
        compare = left
    return filter(lambda x,compare = compare:x in compare,loop)

def Unique(left):
    return reduce(lambda rt,x:x in rt and rt or rt + [x],left,[])
