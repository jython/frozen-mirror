########################################################################
#
# File Name:            Node.py
#
#
"""
Implements the basic tree structure of DOM
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from DOMImplementation import implementation
import Event

from xml.dom import Node, EMPTY_NAMESPACE
from xml.dom import NoModificationAllowedErr
from xml.dom import NamespaceErr
from xml.dom import NotFoundErr
from xml.dom import NotSupportedErr
from xml.dom import HierarchyRequestErr
from xml.dom import WrongDocumentErr
from xml.dom import InvalidCharacterErr
from xml.dom import UnspecifiedEventTypeErr
from xml.dom import XML_NAMESPACE

import re, copy
#FIXME: should allow combining characters: fix when Python gets Unicode
g_pattPrefix = re.compile(r'[a-zA-Z_][\w\.\-_]*\Z')
_namePattern = None
def get_name_pattern():
    # delay creating pattern until it is really needed
    global _namePattern
    if _namePattern: return _namePattern
    try:
        unicode # See whether we have Unicode support
    except NameError:
        _namePattern = re.compile('[a-zA-Z_:][\w\.\-_:]*\Z')
    else:
        import xml.utils.characters
        _namePattern = re.compile(xml.utils.characters.Name+'\Z')
    return _namePattern

class FtNode(Event.EventTarget, Node):
    """
    Encapsulates the pieces that DOM builds on the basic tree structure,
    Which is implemented by composition of TreeNode
    """

    nodeType = None

    # Children that this node is allowed to have
    _allowedChildren = []

    def __init__(self,
                 ownerDocument,
                 namespaceURI=EMPTY_NAMESPACE,
                 prefix=None,
                 localName=None):
        Event.EventTarget.__init__(self)
        self.__dict__['__nodeName'] = None
        self.__dict__['__nodeValue'] = None
        self.__dict__['__parentNode'] = None
        self.__dict__['__childNodes'] = None
        self.__dict__['__previousSibling'] = None
        self.__dict__['__nextSibling'] = None
        self.__dict__['__attributes'] = None
        self.__dict__['__ownerDocument'] = ownerDocument
        self.__dict__['__namespaceURI'] = namespaceURI
        self.__dict__['__prefix'] = prefix
        self.__dict__['__localName'] = localName
        self.__dict__['__childNodes'] = implementation._4dom_createNodeList([])
        self.__dict__['__readOnly'] = 0

    ### Attribute Access Methods -- Node.attr ###

    def __getattr__(self, name):
        attrFunc = self._readComputedAttrs.get(name)
        if attrFunc:
            return attrFunc(self)
        else:
            return getattr(FtNode, name)

    def __setattr__(self, name, value):
        #Make sure attribute is not read-only
        if name in self.__class__._readOnlyAttrs:
            raise NoModificationAllowedErr()
        #If it's computed execute that function
        attrFunc = self.__class__._writeComputedAttrs.get(name)
        if attrFunc:
            attrFunc(self, value)
        #Otherwise, just set the attribute
        else:
            self.__dict__[name] = value

    ### Attribute Methods -- Node._get_attr() ###

    def _get_nodeName(self):
        return self.__dict__['__nodeName']

    def _get_nodeValue(self):
        return self.__dict__['__nodeValue']

    def _set_nodeValue(self,value):
        self.__dict__['__nodeValue'] = value

    def _get_nodeType(self):
        return getattr(self.__class__, 'nodeType')

    def _get_parentNode(self):
        return self.__dict__['__parentNode']

    def _get_childNodes(self):
        return self.__dict__['__childNodes']

    def _get_firstChild(self):
        cn = self.__dict__['__childNodes']
        return cn and cn[0] or None

    def _get_lastChild(self):
        cn = self.__dict__['__childNodes']
        return cn and cn[-1] or None

    def _get_previousSibling(self):
        return self.__dict__['__previousSibling']

    def _get_nextSibling(self):
        return self.__dict__['__nextSibling']

    def _get_ownerDocument(self):
        return self.__dict__['__ownerDocument']

    def _get_attributes(self):
        return self.__dict__['__attributes']

    def _get_namespaceURI(self):
        return self.__dict__['__namespaceURI']

    def _get_prefix(self):
        return self.__dict__['__prefix']

    def _set_prefix(self, value):
        # Check for invalid characters
        if not get_name_pattern().match(value):
            raise InvalidCharacterErr()
        if (self.__dict__['__namespaceURI'] is None or
            ':' in value or
            (value == 'xml' and
             self.__dict__['__namespaceURI'] != XML_NAMESPACE)):
            raise NamespaceErr()
        self.__dict__['__prefix'] = value
        self.__dict__['__nodeName'] = '%s:%s' % (
            value,
            self.__dict__['__localName'])

    def _get_localName(self):
        return self.__dict__['__localName']

    ### Methods ###

    def insertBefore(self, newChild, refChild):
        if refChild is None:
            return self.appendChild(newChild)
        elif newChild.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
            while newChild.firstChild:
                self.insertBefore(newChild.firstChild, refChild)
        else:
            #Make sure the newChild is all it is cracked up to be
            self._4dom_validateNode(newChild)

            #Make sure the refChild is indeed our child
            try:
                index = self.__dict__['__childNodes'].index(refChild)
            except:
                raise NotFoundErr()

            #Remove from old parent
            if newChild.parentNode != None:
                newChild.parentNode.removeChild(newChild);

            #Insert it
            self.__dict__['__childNodes'].insert(index, newChild)

            #Update the child caches
            newChild._4dom_setHierarchy(self, refChild.previousSibling, refChild)

            newChild._4dom_fireMutationEvent('DOMNodeInserted',relatedNode=self)
            self._4dom_fireMutationEvent('DOMSubtreeModified')
        return newChild

    def replaceChild(self, newChild, oldChild):
        if newChild.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
            refChild = oldChild.nextSibling
            self.removeChild(oldChild)
            self.insertBefore(newChild, refChild)
        else:
            self._4dom_validateNode(newChild)
            #Make sure the oldChild is indeed our child
            try:
                index = self.__dict__['__childNodes'].index(oldChild)
            except:
                raise NotFoundErr()

            self.__dict__['__childNodes'][index] = newChild
            if newChild.parentNode is not None:
                newChild.parentNode.removeChild(newChild)

            newChild._4dom_setHierarchy(self,
                                        oldChild.previousSibling,
                                        oldChild.nextSibling)

            oldChild._4dom_fireMutationEvent('DOMNodeRemoved',relatedNode=self)
            oldChild._4dom_setHierarchy(None, None, None)

            newChild._4dom_fireMutationEvent('DOMNodeInserted',relatedNode=self)
            self._4dom_fireMutationEvent('DOMSubtreeModified')
        return oldChild

    def removeChild(self, childNode):
        #Make sure the childNode is indeed our child
        #FIXME: more efficient using list.remove()
        try:
            self.__dict__['__childNodes'].remove(childNode)
        except:
            raise NotFoundErr()
        childNode._4dom_fireMutationEvent('DOMNodeRemoved',relatedNode=self)
        self._4dom_fireMutationEvent('DOMSubtreeModified')

        # Adjust caches
        prev = childNode.previousSibling
        next = childNode.nextSibling
        if prev:
            prev.__dict__['__nextSibling'] = next
        if next:
            next.__dict__['__previousSibling'] = prev

        childNode._4dom_setHierarchy(None, None, None)
        return childNode

    def appendChild(self, newChild):
        if newChild.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
            while newChild.childNodes:
                self.appendChild(newChild.childNodes[0])
        else:
            self._4dom_validateNode(newChild)
            # Remove from old parent
            if newChild.parentNode != None:
                newChild.parentNode.removeChild(newChild);

            last = self.lastChild
            self.childNodes.append(newChild)
            newChild._4dom_setHierarchy(self, last, None)

            newChild._4dom_fireMutationEvent('DOMNodeInserted',relatedNode=self)
            self._4dom_fireMutationEvent('DOMSubtreeModified')
        return newChild

    def hasChildNodes(self):
        return self.__dict__['__childNodes'].length != 0

    def cloneNode(self, deep, newOwner=None, readOnly=0):
        # Get constructor values
        clone = self._4dom_clone(newOwner or self.ownerDocument)

        # Set when cloning EntRef children
        readOnly and clone._4dom_setReadOnly(readOnly)

        # Copy the child nodes if deep
        if deep and self.nodeType != Node.ATTRIBUTE_NODE:
            # Children of EntRefs are cloned readOnly
            if self.nodeType == Node.ENTITY_REFERENCE_NODE:
                readOnly = 1

            for child in self.childNodes:
                new_child = child.cloneNode(1, newOwner, readOnly)
                clone.appendChild(new_child)

        return clone

    def normalize(self):
        # This one needs to join all adjacent text nodes
        node = self.firstChild
        while node:
            if node.nodeType == Node.TEXT_NODE:
                next = node.nextSibling
                while next and next.nodeType == Node.TEXT_NODE:
                    node.appendData(next.data)
                    node.parentNode.removeChild(next)
                    next = node.nextSibling
                if not node.length:
                    # Remove any empty text nodes
                    node.parentNode.removeChild(node)
            elif node.nodeType == Node.ELEMENT_NODE:
                for attr in node.attributes:
                    attr.normalize()
                node.normalize()
            node = node.nextSibling

    def supports(self, feature, version):
        return implementation.hasFeature(feature,version)

    #
    # Event Target interface implementation
    #
    def dispatchEvent(self, evt):
        if not evt.type:
            raise UnspecifiedEventTypeErr()

        # the list of my ancestors for capture or bubbling
        # we are lazy, so we initialize this list only if required
        if evt._4dom_propagate and \
           (evt.eventPhase == evt.CAPTURING_PHASE or evt.bubbles):
            ancestors = [self]
            while  ancestors[-1].parentNode :
                ancestors.append(ancestors[-1].parentNode)

        # event capture
        if evt._4dom_propagate and evt.eventPhase == evt.CAPTURING_PHASE :
            ancestors.reverse()
            for a in ancestors[:-1]:
                evt.currentTarget = a
                for captor in a.capture_listeners[evt.type]:
                    captor.handleEvent(evt)
                if not evt._4dom_propagate:
                    break
            # let's put back the list in the right order
            # and move on to the next phase
            ancestors.reverse()
            evt.eventPhase = evt.AT_TARGET


        # event handling by the target
        if evt._4dom_propagate and evt.eventPhase == evt.AT_TARGET :
            evt.currentTarget = self
            for listener in self.listeners[evt.type]:
                listener.handleEvent(evt)
            # prepare for the next phase, if necessary
            if evt.bubbles:
                evt.eventPhase = evt.BUBBLING_PHASE

        # event bubbling
        if evt._4dom_propagate and evt.eventPhase == evt.BUBBLING_PHASE :
            for a in ancestors[1:]:
                evt.currentTarget = a
                for listener in a.listeners[evt.type]:
                    listener.handleEvent(evt)
                if not evt._4dom_propagate:
                    break

        return evt._4dom_preventDefaultCalled


    ### Unsupported, undocumented DOM Level 3 methods ###
    ### documented in the Python binding ###

    def isSameNode(self, other):
        return self == other

    ### Internal Methods ###

    #Functions not defined in the standard
    #All are fourthought internal functions
    #and should only be called by you if you specifically
    #don't want your program to run :)

    def _4dom_setattr(self, name, value):
        self.__dict__[name] = value

    def _4dom_fireMutationEvent(self,eventType,target=None,
                                 relatedNode=None,prevValue=None,
                                 newValue=None,attrName=None,attrChange=None):
        if self.supports('MutationEvents', 2.0):
            evt = self.ownerDocument.createEvent(eventType)
            evt.target = target or self
            evt.initMutationEvent(eventType,evt.eventSpec[eventType],0,
                                  relatedNode,prevValue,newValue,attrName)
            evt.attrChange = attrChange
            evt.target.dispatchEvent(evt)

    def _4dom_validateNode(self, newNode):
        if not newNode.nodeType in self.__class__._allowedChildren:
            raise HierarchyRequestErr()
        self._4dom_raiseIfAncestor(newNode)
        if self.ownerDocument != newNode.ownerDocument:
            raise WrongDocumentErr()

    def _4dom_raiseIfAncestor(self, node):
        "Helper function that raises if node is an ancestor of self or self."
        n = self
        if n is node:
            raise HierarchyRequestErr()
        if node.hasChildNodes():
            while n is not None:
                n = n.parentNode
                if n is node:
                    raise HierarchyRequestErr()

    def _4dom_setHierarchy(self, parent, previous, next):
        self.__dict__['__parentNode'] = parent
        if previous:
            previous.__dict__['__nextSibling'] = self
        self.__dict__['__previousSibling'] = previous
        self.__dict__['__nextSibling'] = next
        if next:
            next.__dict__['__previousSibling'] = self
        return

    def _4dom_setParentNode(self, parent):
        self.__dict__['__parentNode'] = parent

    def _4dom_setNextSibling(self,next):
        self.__dict__['__nextSibling'] = next

    def _4dom_setPreviousSibling(self,prev):
        self.__dict__['__previousSibling'] = prev

    def _4dom_setOwnerDocument(self, owner):
        self.__dict__['__ownerDocument'] = owner

    def _4dom_setReadOnly(self, flag):
        self.__dict__['__readOnly'] = flag

    ### Helper Functions For Cloning ###

    def _4dom_clone(self, owner):
        raise NotSupportedErr('Subclass must override')

    def __getinitargs__(self):
        return (self.__dict__['__ownerDocument'],
                self.__dict__['__namespaceURI'],
                self.__dict__['__prefix'],
                self.__dict__['__localName']
                )

    def __getstate__(self):
        return self.__dict__['__childNodes']

    def __setstate__(self, children):
        self.__dict__['__childNodes'].extend(list(children))
        prev = None
        for child in children:
            child._4dom_setHierarchy(self, prev, None)
            prev = child

    ### Attribute Access Mappings ###

    _readComputedAttrs = {'nodeName':_get_nodeName,
                          'nodeValue':_get_nodeValue,
                          'nodeType':_get_nodeType,
                          'parentNode':_get_parentNode,
                          'childNodes':_get_childNodes,
                          'firstChild':_get_firstChild,
                          'lastChild':_get_lastChild,
                          'previousSibling':_get_previousSibling,
                          'nextSibling':_get_nextSibling,
                          'attributes':_get_attributes,
                          'ownerDocument':_get_ownerDocument,
                          'namespaceURI':_get_namespaceURI,
                          'prefix':_get_prefix,
                          'localName':_get_localName
                          }

    _writeComputedAttrs = {'nodeValue':_set_nodeValue,
                           'prefix':_set_prefix
                           }

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            _readComputedAttrs.keys())
