########################################################################
#
# File Name:            CharacterData.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import Node
from DOMImplementation import implementation
from FtNode import FtNode

from ext import IsDOMString

from xml.dom import IndexSizeErr
from xml.dom import SyntaxErr

class CharacterData(FtNode):
    def __init__(self, ownerDocument, data):
        FtNode.__init__(self, ownerDocument)
        self.__dict__['__nodeValue'] = data
        self._length = len(data)

    ### Attribute Methods ###

    def _get_data(self):
        return self.__dict__['__nodeValue']

    def _set_data(self, data):
        if not IsDOMString(data):
            raise SyntaxErr()
        old_value = self.__dict__['__nodeValue']
        self.__dict__['__nodeValue'] = data
        self._length = len(data)
        self._4dom_fireMutationEvent('DOMCharacterDataModified',
                                     prevValue=old_value,
                                     newValue=data)

    def _get_length(self):
        return self._length

    ### Methods ###

    def appendData(self, arg):
        if len(arg):
            self._set_data(self.__dict__['__nodeValue'] + arg)
            self._4dom_fireMutationEvent('DOMSubtreeModified')
        return

    def deleteData(self, offset, count):
        if count < 0 or offset < 0 or offset > self._length:
            raise IndexSizeErr()
        data = self.__dict__['__nodeValue']
        data = data[:int(offset)] + data[int(offset+count):]
        self._set_data(data)
        self._4dom_fireMutationEvent('DOMSubtreeModified')
        return

    def insertData(self, offset, arg):
        if offset < 0 or offset > self._length:
            raise IndexSizeErr()
        if not IsDOMString(arg):
            raise SyntaxErr()
        data = self.__dict__['__nodeValue']
        data = data[:int(offset)] + arg + data[int(offset):]
        self._set_data(data)
        self._4dom_fireMutationEvent('DOMSubtreeModified')
        return

    def replaceData(self, offset, count, arg):
        if not IsDOMString(arg):
            raise SyntaxErr()
        if count < 0 or offset < 0 or offset > self._length:
            raise IndexSizeErr()
        data = self.__dict__['__nodeValue']
        data = data[:int(offset)] + arg + data[int(offset+count):]
        self._set_data(data)
        self._4dom_fireMutationEvent('DOMSubtreeModified')
        return

    def substringData(self, offset, count):
        if count < 0 or offset < 0 or offset > self._length:
            raise IndexSizeErr()
        return self.data[int(offset):int(offset+count)]

    ### Helper Functions For Cloning ###

    def _4dom_clone(self, owner):
        return self.__class__(owner, self.data)

    def __getinitargs__(self):
        return (self.ownerDocument,
                self.data
                )

    ### Overridden Methods ###

    def __repr__(self):
        # Trim to a managable size
        if len(self.data) > 20:
            data = self.data[:20] + '...'
        else:
            data = self.data

        # Escape unprintable chars
        import string
        for ws in ['\t','\n','\r']:
            data = string.replace(data, ws, '\\0x%x' % ord(ws))

        return "<%s Node at %x: %s>" % (
            self.__class__.__name__,
            id(self),
            repr(data))

    ### Attribute Access Mappings ###

    _readComputedAttrs = FtNode._readComputedAttrs.copy()
    _readComputedAttrs.update({
        'length':_get_length,
        'data':_get_data
        })


    _writeComputedAttrs = FtNode._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
        'data':_set_data
        })

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            FtNode._readOnlyAttrs + _readComputedAttrs.keys())
