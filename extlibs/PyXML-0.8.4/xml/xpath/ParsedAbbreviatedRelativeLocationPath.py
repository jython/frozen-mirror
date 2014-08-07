########################################################################
#
# File Name:   ParsedAbbreviatedRelativeLocationPath.py
#
#
"""
A parsed token that represents a abbreviated relative location path.
WWW: http://4suite.org/XPATH        e-mail: support@4suite.org

Copyright (c) 2000-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

from xml.xpath import ParsedNodeTest
from xml.xpath import ParsedPredicateList
from xml.xpath import ParsedAxisSpecifier
from xml.xpath import ParsedStep

import Set

class ParsedAbbreviatedRelativeLocationPath:
    def __init__(self,left,right):
        """
        left can be a step or a relative location path
        right is only a step
        """
        self._left = left
        self._right = right
        nt = ParsedNodeTest.ParsedNodeTest('node','')
        ppl = ParsedPredicateList.ParsedPredicateList([])
        as = ParsedAxisSpecifier.ParsedAxisSpecifier('descendant-or-self')
        self._middle = ParsedStep.ParsedStep(as, nt, ppl)

    def evaluate(self, context):
        res = []
        rt = self._left.select(context)
        l = len(rt)

        origState = context.copyNodePosSize()

        for ctr in range(l):
            context.setNodePosSize((rt[ctr],ctr+1,l))
            subRt = self._middle.select(context)
            res = Set.Union(res,subRt)

        rt = res
        res = []
        l = len(rt)
        for ctr in range(l):
            context.setNodePosSize((rt[ctr],ctr+1,l))
            subRt = self._right.select(context)
            res = Set.Union(res,subRt)


        context.setNodePosSize(origState)
        return res
    select = evaluate

    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._middle.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def __str__(self):
        return '<AbbreviatedRelativeLocationPath at %x: %s>' % (
            id(self),
            repr(self),
            )
    def __repr__(self):
        return repr(self._left) + '//' + repr(self._right)
