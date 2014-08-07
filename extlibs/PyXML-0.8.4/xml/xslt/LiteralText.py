########################################################################
#
# File Name:            LiteralText.py
#
#
"""
Implementation of the XSLT Spec import stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""
import string
try:
    from Ft.Lib import pDomlette
    _Base = pDomlette.Text
    def _base_init(self, doc, data):
        _Base.__init__(self, doc)
except ImportError:
    from xml.dom import minidom
    _Base = minidom.Text
    def _base_init(self, doc, data):
        _Base.__init__(self, data)

class LiteralText(_Base):
    def __init__(self, doc, data):
        _base_init(self, doc, data)
        self.data = data

    def setup(self):
        return

    def instantiate(self, context, processor):
        processor.writers[-1].text(self.data)
        return (context,)

    def __getinitargs__(self):
        return (None, self.data)

