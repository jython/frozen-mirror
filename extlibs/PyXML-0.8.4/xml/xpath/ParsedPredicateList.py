########################################################################
#
# File Name:   ParsedPredicateList.py
#
#
"""
A Parsed Token that represents a predicate list.
WWW: http://4suite.org/XPATH        e-mail: support@4suite.org

Copyright (c) 2000-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

from xml.xpath import Conversions
import types
NumberTypes = [types.IntType, types.LongType, types.FloatType]


class ParsedPredicateList:
    def __init__(self, preds):
        if type(preds) == type(()):
            preds = list(preds)
        elif not type(preds) == type([]):
            raise "Invalid Predicates: ",str(preds)

        self._predicates = preds
        self._length = len(preds)

    def append(self,pred):
        self._predicates.append(pred)
        self._length = self._length + 1

    def filter(self, nodeList, context, reverse):
        if self._length:
            state = context.copyNodePosSize()
            for pred in self._predicates:
                size = len(nodeList)
                ctr = 0
                current = nodeList
                nodeList = []
                for node in current:
                    position = (reverse and size - ctr) or (ctr + 1)
                    context.setNodePosSize((node, position, size))
                    res = pred.evaluate(context)
                    if type(res) in NumberTypes:
                        # This must be separate to prevent falling into
                        # the boolean check.
                        if res == position:
                            nodeList.append(node)
                    elif Conversions.BooleanValue(res):
                        nodeList.append(node)
                    ctr = ctr + 1
            context.setNodePosSize(state)
        return nodeList

    def __getitem__(self, index):
        return self._predicates[index]

    def __len__(self):
        return self._length

    def pprint(self, indent=''):
        print indent + str(self)
        for pred in self._predicates:
            pred.pprint(indent + '  ')

    def __str__(self):
        return '<PredicateList at %x: %s>' % (
            id(self),
            repr(self) or '(empty)',
            )

    def __repr__(self):
        return reduce(lambda result, pred:
                      result + '[%s]' % repr(pred),
                      self._predicates,
                      ''
                      )
