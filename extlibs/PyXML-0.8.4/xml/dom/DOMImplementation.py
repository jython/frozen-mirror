########################################################################
#
# File Name:            DOMImplementation.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string

FEATURES_MAP = {'CORE':2.0,
                'XML':2.0,
                'TRAVERSAL':2.0,
                'EVENTS':2.0,
                'MUTATIONEVENTS':2.0,
                }

try:
    import Range
except:
    pass
else:
    FEATURES_MAP['RANGE'] = 2.0

class DOMImplementation:

    def __init__(self):
        pass

    def hasFeature(self, feature, version=''):
        featureVersion = FEATURES_MAP.get(string.upper(feature))
        if featureVersion:
            if version and float(version) != featureVersion:
                return 0
            return 1
        return 0

    def createDocumentType(self, qualifiedName, publicId, systemId):
        import DocumentType
        dt = DocumentType.DocumentType(qualifiedName,
                                       self._4dom_createNamedNodeMap(),
                                       self._4dom_createNamedNodeMap(),
                                       publicId,
                                       systemId)
        return dt

    def createDocument(self, namespaceURI, qualifiedName, doctype):
        import Document
        doc = Document.Document(doctype)
        if qualifiedName:
            el = doc.createElementNS(namespaceURI, qualifiedName)
            doc.appendChild(el)
        return doc

    def _4dom_createNodeList(self, list=None):
        import NodeList
        return NodeList.NodeList(list)

    def _4dom_createNamedNodeMap(self, owner=None):
        import NamedNodeMap
        return NamedNodeMap.NamedNodeMap(owner)

implementation = DOMImplementation()
getDOMImplementation = DOMImplementation
