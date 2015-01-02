import string, urllib, urllib2, StringIO, xml.sax.sax2exts, xml.sax.handler
from xml.dom import minidom,pulldom, EMPTY_NAMESPACE

# _XsltElementBase is used when Ft.Lib.pDomlette.Element is not available

class _XsltElementBase(minidom.Element):
    def __init__(self, ownerDocument, namespaceURI=EMPTY_NAMESPACE, localName='', prefix=''):
        if prefix:
            tagName = prefix+':'+localName
        else:
            tagName = localName
        minidom.Element.__init__(self, tagName, namespaceURI, prefix, localName)
        self.ownerDocument = ownerDocument

    def __getstate__(self):
        return (self.childNodes, self.parentNode, self.ownerDocument,
                self.tagName, self.nodeName, self.prefix,
                self.namespaceURI, self.nodeValue, self._attrs,
                self._attrsNS)

    def __setstate__(self, st):
        (self.childNodes, self.parentNode, self.ownerDocument,
         self.tagName, self.nodeName, self.prefix, self.namespaceURI,
         self.nodeValue, self._attrs, self._attrsNS) = st


# _ReaderBase is used in StylesheetReader if
# Ft.Lib.ReaderBase.DomletteReader is not available

import StringIO
class _ReaderBase:
    def __init__(self, force8Bit = 0):
        self.force8Bit = force8Bit

    def clone(self):
        if hasattr(self,'__getinitargs__'):
            return apply(self.__class__,self.__getinitargs__())
        else:
            return self.__class__()

    def initState(self, ownerDoc=None, stripElements=None):
        self._preserveStateStack = [1]
        self._stripElements = stripElements or []
        if ownerDoc:
            self._ownerDoc = ownerDoc
            #Create a docfrag to hold all the generated nodes.
            self._rootNode = doc.createDocumentFragment()
        else:
            self._rootNode = self._ownerDoc = minidom.Document()
        #Set up the stack which keeps track of the nesting of DOM nodes.
        self._nodeStack = [self._rootNode]
        self._namespaces = [{'xml': XML_NAMESPACE}]
        self._currText = ''

    def fromUri(self, uri, baseUri = '',  ownerDoc=None, stripElements=None):
        url = urllib.basejoin(baseUri, uri)
        stream = urllib2.urlopen(url)
        return self.fromStream(stream, baseUri, ownerDoc, stripElements)

    def fromString(self, st, baseUri='', ownerDoc=None, stripElements=None):
        st = StringIO.StringIO(st)
        return self.fromStream(st, baseUri, ownerDoc, stripElements)

# g_readerClass is used in Processor if Ft.Lib.pDomlette.PyExpatReader
# is not available

class StrippingPullDOM(pulldom.PullDOM):
    def __init__(self, stripElements):
        pulldom.PullDOM.__init__(self)
        self.stripElements = stripElements or []
        self.stripState = [1]
        self._currText = ''

    def startElementNS(self, name, tagName , attrs):
        self._completeTextNode()
        pulldom.PullDOM.startElementNS(self, name, tagName, attrs)
        new_element = self.elementStack[-1]
        new_pstate = self.stripState[-1]
        for (uri, local, strip) in self.stripElements:
            if (uri, local) in [(new_element.namespaceURI, new_element.localName), (EMPTY_NAMESPACE, '*'), (new_element.namespaceURI, '*')]:
                new_pstate = not strip
                break
        self.stripState.append(new_pstate)

    def endElementNS(self, name, tagName):
        self._completeTextNode()
        pulldom.PullDOM.endElementNS(self, name, tagName)
        del self.stripState[-1]

    def startElement(self, name, attrs):
        raise NotImplemented

    def endElement(self, name):
        raise NotImplemented

    def _completeTextNode(self):
        if self._currText and self.document:
            if self.stripState[-1] or string.strip(self._currText):
                pulldom.PullDOM.characters(self, self._currText)
        self._currText = ''

    def characters(self, data):
        self._currText = self._currText + data

    def ignorableWhitespace(self, data):
        self._currText = self._currText + data

    def processingInstruction(self, target, data):
        self._completeTextNode()
        return pulldom.PullDOM.processingInstruction(self, target, data)

    def comment(self, data):
        self._completeTextNode()
        return pulldom.PullDOM.comment(self, data)

class StrippingStream(pulldom.DOMEventStream):
    def __init__(self, stream, parser, bufsize, stripElements):
        self.stream = stream
        self.parser = parser
        self.bufsize = bufsize
        self.pulldom = StrippingPullDOM(stripElements)
        # This content handler relies on namespace support
        self.parser.setFeature(xml.sax.handler.feature_namespaces, 1)
        self.parser.setContentHandler(self.pulldom)

class MinidomReader(_ReaderBase):
    def __init__(self, validate = 0):
        self.validate = validate
        
    def fromStream(self, stream, baseUri='',ownerDoc=None, stripElements=None):
        if self.validate:
            parser = xml.sax.sax2exts.XMLValParserFactory.make_parser()
        else:
            parser = xml.sax.sax2exts.XMLParserFactory.make_parser()
        events = StrippingStream(stream, parser, pulldom.default_bufsize, stripElements)
        toktype, rootNode = events.getEvent()
        events.expandNode(rootNode)
        events.clear()
        return rootNode

    def releaseNode(self, n):
        n.unlink()
