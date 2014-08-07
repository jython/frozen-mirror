########################################################################
#
# File Name:            implementation.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import DOMImplementation

# Add the HTML feature
DOMImplementation.FEATURES_MAP['HTML'] = 2.0

class HTMLDOMImplementation(DOMImplementation.DOMImplementation):

    def __init__(self):
        DOMImplementation.DOMImplementation.__init__(self)

    def createHTMLDocument(self, title):
        from xml.dom.html import HTMLDocument
        doc = HTMLDocument.HTMLDocument()
        h = doc.createElement('HTML')
        doc.appendChild(h)
        doc._set_title(title)
        return doc

    def _4dom_createHTMLCollection(self,list=None):
        if list is None:
            list = []
        from xml.dom.html import HTMLCollection
        hc = HTMLCollection.HTMLCollection(list)
        return hc
