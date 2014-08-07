########################################################################
#
# File Name:   ParsedRelativeLocationPath.py
#
#
"""
A Parsed Token that represents a relative location path in the parsed result tree.
WWW: http://4suite.org/XPATH        e-mail: support@4suite.org

Copyright (c) 2000-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

class ParsedRelativeLocationPath:
    def __init__(self, left, right):
        self._left = left
        self._right = right
        return

    def evaluate(self, context):
        rt = self._left.select(context)
        if type(rt) != type([]):
            raise Exception("Expected node set from relative expression.  Got %s"%str(rt))

        origState = context.copyNodePosSize()

        result = []
        l = len(rt)
        for ctr in range(l):
            n = rt[ctr]
            context.setNodePosSize((n, ctr+1, l))
            result.extend(self._right.select(context))

        context.setNodePosSize(origState)

        return result
    select = evaluate

    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def __str__(self):
        return '<RelativeLocationPath at %x: %s>' % (
            id(self),
            repr(self),
            )

    def __repr__(self):
        return repr(self._left) + '/' + repr(self._right)
