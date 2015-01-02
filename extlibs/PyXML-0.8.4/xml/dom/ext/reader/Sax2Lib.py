"""A Python translation of the SAX2 parser API. This file provides only
default classes with absolutely minimum functionality, from which
drivers and applications can be subclassed.

Many of these classes are empty and are included only as documentation
of the interfaces.
"""

from xml.sax import saxlib

class LexicalHandler:
    """
    Default handler for lexical events
    Note: All methods can raise SAXException
    """
    handlerId = 'http://xml.org/sax/handlers/lexical'

    def xmlDecl(self, version, encoding, standalone):
        """The XML Declaration"""
        pass

    def startDTD(self, doctype, publicID, systemID):
        """Invoked at the beginning of the DOCTYPE declaration"""
        pass

    def endDTD(self):
        """
        Invoked after all components of the DOCTYPE declaration,
        including both internal and external DTD subsets
        """
        pass

    def startEntity(self, name):
        """
        Note: If an external DTD subset is read, it will invoke this method
        with special entity name of "[DTD]"
        """
        pass

    def endEntity(self, name):
        pass

    def comment(self, text):
        """XML Comment"""
        pass

    def startCDATA(self):
        """Beginning of CDATA Section"""
        pass

    def endCDATA(self):
        """End of CDATA Section"""
        pass


class  AttributeList2(saxlib. AttributeList):
    def isSpecified(self, id):
        """
        Whether the attribute value with the given name or index was
        explicitly specified in the element, or was determined from the
        default.  Parameter can be either integer index or attribute name.
        None (the default) signals 'Don't Know', else a boolean return
        """
        pass

    def getEntityRefList(self, id):
        """
        XML 1,0 parsers are required to report all entity references,
        even if unexpanded.  This includes those in attribute strings.
        Many parsers and apps ignore this, but for full conformance,
        This method can be called to get a list of indexes referring
        to entity references within the attribute value string for the
        given name or index.  Parameter can be either integer index or
        attribute name.
        """
        pass


class EntityRefList:
    """
    This is the entity-reference list returned by
    AttributeList2.getEntityRefList(index)
    """
    def getLength(self):
        "Return the number of Entity Ref pointers"
        pass

    def getEntityName(self, index):
        "Return the name of the entity reference at the given index"
        pass

    def getEntityRefStart(self, index):
        """
        Return the string start position of the entity reference
        at the given index
        """
        pass

    def getEntityRefEnd(self, index):
        """
        Return the string end position of the entity reference
        at the given index
        """
        pass

    def __len__(self):
        "Alias for getLength."
        pass


class DTDDeclHandler:
    """
    A handler for a minimal set of DTD Events
    """
    MODEL_ELEMENTS = 1
    MODEL_MIXED = 2
    MODEL_ANY = 3
    MODEL_EMPTY = 4
    ATTRIBUTE_DEFAULTED = 1
    ATTRIBUTE_IMPLIED = 2
    ATTRIBUTE_REQUIRED = 3
    ATTRIBUTE_FIXED = 4

    handlerId = 'http://xml.org/sax/handlers/dtd-decl'

    def elementDecl(self, name, modelType, model):
        """
        Report an element-type declaration.
        name and model are strings, modelType is an enumerated int from 1 to 4
        """
        pass

    def attributeDecl(self,
                      element,
                      name,
                      type,
                      defaultValue,
                      defaultType,
                      entityRefs):
        """
        Report an attribute declaration.  The first 4 parameters are strings,
        defaultType is an integer from 1 to 4, entityRefs is an EntityRefList
        """
        pass

    def externalEntityDecl(self, name, isParameterEntity, publicId, systemId):
        """
        Report an external entity declaration.
        All parameters are strings except for isParameterEntity,
        which is 0 or 1
        """
        pass

    def internalEntityDecl(self, name, isParameterEntity, value):
        """
        Report an external entity declaration.
        All parameters are strings except for isParameterEntity,
        which is 0 or 1
        """
        pass


class NamespaceHandler:
    """
    Receive callbacks for the start and end of the scope of each
    namespace declaration.
    """

    handlerId = 'http://xml.org/sax/handlers/namespace'

    def startNamespaceDeclScope(self, prefix, uri):
        """
        Report the start of the scope of a namespace declaration.
        This event will be reported before the startElement event
        for the element containing the namespace declaration.  All
        declarations must be properly nested; if there are multiple
        declarations in a single element, they must end in the opposite
        order that they began.
        both parameters are strings
        """
        pass

    def endNamespaceDeclScope(self, prefix):
        """
        Report the end of the scope of a namespace declaration.
        This event will be reported after the endElement event for
        the element containing the namespace declaration.  Namespace
        scopes must be properly nested.
        """
        pass


class ModParser(saxlib.Parser):
    """
    All methods may raise
    SAXNotSupportedException
    """
    def setFeature(self, featureID, state):
        """
        featureId is a string, state a boolean
        """
        pass

    def setHandler(self, handlerID, handler):
        """
        handlerID is a string, handler a handler instance
        """
        pass

    def set(self, propID, value):
        """
        propID is a string, value of arbitrary type
        """
        pass

    def get(self, propID):
        pass


import sys
if sys.platform[0:4] == 'java':
    from exceptions import Exception

class SAXNotSupportedException(Exception):
    """
    Indicate that a SAX2 parser interface does not support a particular
    feature or handler, or property.
    """
    pass


#Just a few helper lists with the core components
CoreHandlers = [
'http://xml.org/sax/handlers/lexical',
'http://xml.org/sax/handlers/dtd-decl',
'http://xml.org/sax/handlers/namespace'
]

CoreProperties = [
'http://xml.org/sax/properties/namespace-sep',
#write-only string
#Set the separator to be used between the URI part of a name and the
#local part of a name when namespace processing is being performed
#(see the http://xml.org/sax/features/namespaces feature).  By
#default, the separator is a single space.  This property may not be
#set while a parse is in progress (raises SAXNotSupportedException).

'http://xml.org/sax/properties/dom-node',
#read-only Node instance
#Get the DOM node currently being visited, if the SAX parser is
#iterating over a DOM tree.  If the parser recognises and supports
#this property but is not currently visiting a DOM node, it should
#return null (this is a good way to check for availability before the
#parse begins).

'http://xml.org/sax/properties/xml-string'
#read-only string
#Get the literal string of characters associated with the current
#event.  If the parser recognises and supports this property but is
#not currently parsing text, it should return null (this is a good
#way to check for availability before the parse begins).
]

CoreFeatures = [
'http://xml.org/sax/features/validation',
#Validate (1) or don't validate (0).

'http://xml.org/sax/features/external-general-entities',
#Expand external general entities (1) or don't expand (0).

'http://xml.org/sax/features/external-parameter-entities',
#Expand external parameter entities (1) or don't expand (0).

'http://xml.org/sax/features/namespaces',
#Preprocess namespaces (1) or don't preprocess (0).  See also

#the http://xml.org/sax/properties/namespace-sep property.
'http://xml.org/sax/features/normalize-text'
#Ensure that all consecutive text is returned in a single callback to
#DocumentHandler.characters or DocumentHandler.ignorableWhitespace
#(1) or explicitly do not require it (0).
]
