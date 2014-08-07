########################################################################
#
# File Name:            XsltContext.py
#
#
"""
Provide contextual and state information wrt the transform processing
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.xpath import Context, Util
from xml.xslt import XsltFunctions, ReleaseNode


#Note: Some of the state information maintained here would probably be better
#managed by the processor, but until Python is less prone to circular reference
#Traps, the current arrangement will have to do

class XsltContext(Context.Context):
    functions = Context.Context.functions.copy()
    functions.update(XsltFunctions.ExtFunctions)

    def __init__(self,
                 node,
                 position=1,
                 size=1,
                 currentNode=None,
                 varBindings=None,
                 processorNss=None,
                 stylesheet=None,
                 processor=None,
                 mode=None):
        Context.Context.__init__(self,
                                 node,
                                 position,
                                 size,
                                 varBindings,
                                 processorNss)
        self.currentNode = currentNode
        self.stylesheet = stylesheet
        self.mode = mode
        self.processor = processor
        self.currentInstruction = None
        self.documents = {}
        self.rtfs = []
        return

    def copyNodePosSizeMode(self):
        return (self.node, self.position, self.size, self.mode)

    def setNodePosSizeMode(self, args):
        self.node = args[0]
        self.position = args[1]
        self.size = args[2]
        self.mode = args[3]

    def setStylesheet(self, args):
        self.varBindings = args[0]
        self.processorNss.update(args[1])
        self.stylesheet = args[2]

    def copyStylesheet(self):
        return (self.varBindings, self.processorNss, self.stylesheet)

    def release(self):
        Util.FreeDocumentIndex(self.node)
        for doc in self.documents.values():
            Util.FreeDocumentIndex(doc)
            ReleaseNode(doc)
        try:
            for rtf in self.rtfs:
                ReleaseNode(rtf)
        except:
            import traceback
            traceback.print_exc()
            pass
        self.documents = None
        self.rtfs = None
        return


    def set(self,d):
        d['documents'].update(self.documents)
        d['rtfs'] = self.rtfs
        Context.Context.set(self,d)


    def clone(self):
        return XsltContext(self.node, self.position, self.size,
                           self.currentNode, self.varBindings,
                           self.processorNss, self.stylesheet,
                           self.processor, self.mode)

    def __repr__(self):
        return '<XsltContext at %x: Node=%s, Position="%d", Size="%d">' % (
            id(self),
            repr(self.node),
            self.position,
            self.size
            )

