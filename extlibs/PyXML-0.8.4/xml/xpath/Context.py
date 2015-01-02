########################################################################
#
# File Name:   Context.py
#
#
"""
The context of an XPath expression.
WWW: http://4suite.org/XPATH        e-mail: support@4suite.org

Copyright (c) 2000-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

import xml.dom.ext
import CoreFunctions

class Context:
    functions = CoreFunctions.CoreFunctions

    def __init__(self,
                 node,
                 position=1,
                 size=1,
                 varBindings=None,
                 processorNss=None):
        self.node = node
        self.position = position
        self.size = size
        self.varBindings = varBindings or {}
        self.processorNss = processorNss or {}
        self._cachedNss = None
        self._cachedNssNode = None
        self.stringValueCache = {}
        return

    def __repr__(self):
        return "<Context at %s: Node=%s, Postion=%d, Size=%d>" % (
            id(self),
            self.node,
            self.position,
            self.size
            )

    def nss(self):
        if self._cachedNss is None or self.node != self._cachedNssNode:
            nss = xml.dom.ext.GetAllNs(self.node)
            self._cachedNss = nss
            self._cachedNssNode = self.node
        return self._cachedNss

    def next(self):
        pass

    def setNamespaces(self, processorNss):
        self.processorNss = processorNss

    def copyNamespaces(self):
        return self.processorNss.copy()

    def setVarBindings(self, varBindings):
        self.varBindings = varBindings

    def copyVarBindings(self):
        #FIXME: should this be deep copy, because of the possible list entries?
        return self.varBindings.copy()

    def copyNodePosSize(self):
        return (self.node, self.position, self.size)

    def setNodePosSize(self,(node,pos,size)):
        self.node = node
        self.position = pos
        self.size = size

    def copy(self):
        newdict = self.__dict__.copy()
        newdict["varBindings"] = self.varBindings.copy()
        return newdict

    def set(self,d):
        self.__dict__ = d

