########################################################################
#
# File Name:            ProcessingInstruction.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import Node, EMPTY_NAMESPACE
from FtNode import FtNode

class ProcessingInstruction(FtNode):
    nodeType = Node.PROCESSING_INSTRUCTION_NODE

    def __init__(self,ownerDocument,target,data):
        FtNode.__init__(self,ownerDocument,EMPTY_NAMESPACE,'','')
        self.__dict__['__nodeName'] = target
        self.__dict__['__nodeValue'] = data

    def _get_target(self):
        return self.__dict__['__nodeName']

    def _get_data(self):
        return self.__dict__['__nodeValue']

    def _set_data(self, newData):
        self.__dict__['__nodeValue'] = newData

    ### Overridden Methods ###

    def __repr__(self):
        data = self.data
        if len(data) > 20:
            data = data[20:] + '...'
        return "<ProcessingInstruction at %x: target='%s' data='%s'>" % (
            id(self),
            self.target,
            data
            )

    ### Helper Functions For Cloning ###

    def _4dom_clone(self, owner):
        return self.__class__(owner, self.target, self.data)

    def __getinitargs__(self):
        return (self.ownerDocument,
                self.target,
                self.data
                )

    ### Attribute Access Mappings ###

    _readComputedAttrs = FtNode._readComputedAttrs.copy()
    _readComputedAttrs.update({'target':_get_target,
                               'data':_get_data
                               })


    _writeComputedAttrs = FtNode._writeComputedAttrs.copy()
    _writeComputedAttrs.update({'data':_set_data
                                })

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            FtNode._readOnlyAttrs + _readComputedAttrs.keys())
