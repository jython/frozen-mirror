"""  parser to generate SAX events from a DOM tree

$Date: 2002/05/02 10:15:04 $ by $Author: loewis $
"""

from xml.sax._exceptions import SAXNotSupportedException, SAXNotRecognizedException
from xml.sax.xmlreader import XMLReader, AttributesNSImpl, AttributesImpl
from xml.sax.saxlib import LexicalHandler, DeclHandler
from xml.sax import handler
from xml.dom import Node, XMLNS_NAMESPACE
XMLNS_NS = XMLNS_NAMESPACE

class Dom2SaxParser(XMLReader):
    """  Generate SAX events from a DOM tree
    
    handle _ feature_namespaces
           _ feature_namespace_prefixes,
           _ property_lexical_handler
           _ property_declaration_handler (not yet fully)
           
    differences with standard sax parser:
         _ no error handling (we start from a dom tree !!)
         _ no locator (same reason)
    """
    def __init__(self):
        XMLReader.__init__(self)
        self._lex_handler = LexicalHandler()
        self._decl_handler = DeclHandler()
        self._ns = 0
        self._ns_prfx = 1
        self._parsing = 0

        
    ## properties and features ##################################################
    def getFeature(self, name):
        if name == handler.feature_namespaces:
            return self._ns
        elif name == handler.feature_namespace_prefixes:
            return self._ns_prfx
        raise SAXNotRecognizedException("Feature '%s' not recognized"%name)

    
    def setFeature(self, name, state):
        if self._parsing:
            raise SAXNotSupportedException("Cannot set features while parsing")
        
        if name == handler.feature_namespaces:
            self._ns = state
        elif name == handler.feature_namespace_prefixes:
            self._ns_prfx = state
        else:
            raise SAXNotRecognizedException("Feature '%s' not recognized"%name)

        
    def getProperty(self, name):
        if name == handler.property_lexical_handler:
            return self._lex_handler_prop
        if name == handler.property_declaration_handler:
            return self._decl_handler_prop
        raise SAXNotRecognizedException("Property '%s' not recognized"%name)

    
    def setProperty(self, name, value):
        if self._parsing:
            raise SAXNotSupportedException("Cannot set properties while parsing")
        
        if name == handler.property_lexical_handler:
            self._lex_handler = value
        elif name == handler.property_declaration_handler:
            self._decl_handler = value
        else:
            raise SAXNotRecognizedException("Property '%s' not recognized"%name)

        
    ##  parsing ################################################################
    def parse(self, dom):
        if self._parsing:
            raise SAXNotSupportedException("Ask for parse while parsing")
        
        self._parsing = 1
        if self._ns: self._element_ = self._element_ns
        else: self._element_ = self._element
        self._from_dom(dom)
        self._parsing = 0


    ## private #################################################################
    def _from_dom(self, n):
        while n:
            type = n.nodeType
            if type == Node.ELEMENT_NODE:
                self._element_(n)
            elif type == Node.TEXT_NODE:
                self._cont_handler.characters(n.data)
            elif type == Node.PROCESSING_INSTRUCTION_NODE:
                self._cont_handler.processingInstruction(n.target, n.data)
            elif type == Node.DOCUMENT_NODE:
                self._cont_handler.startDocument()
                self._from_dom(n.firstChild)
                self._cont_handler.endDocument()
            elif type == Node.DOCUMENT_FRAGMENT_NODE:
                for n in n.childNodes:
                    self._cont_handler.startDocument()
                    self._from_dom(n.firstChild)
                    self._cont_handler.endDocument()
            elif type == Node.CDATA_SECTION_NODE:
                self._lex_handler.startCDATA()
                self._cont_handler.characters(n.data)
                self._lex_handler.endCDATA()
            elif type == Node.COMMENT_NODE:
                self._lex_handler.comment(n.data)
            elif type == Node.DOCUMENT_TYPE_NODE:
                self._lex_handler.startDTD(n.name, n.publicId, n.systemId)
                for i in range(n.entities.length):
                    e = n.entities.item(i)
                    if e.publicId or e.systemId:
                        self._decl_handler.externalEntityDecl(
                            e.notationName, e.publicId, e.systemId)
                    else:
                        self._decl_handler.externalEntityDecl(
                            e.name, e.value)
                self._lex_handler.endDTD()
            elif type == Node.ENTITY_REFERENCE_NODE:
                self._lex_handler.startEntity(n.nodeName)
                self._from_dom(n.firstChild)
                self._lex_handler.endEntity(n.nodeName)
            #elif type == Node.ENTITY_NODE:
            #elif type == Node.NOTATION_NODE:
            n = n.nextSibling

  
    def _element(self, n):
        """ handle an ElementNode without NS interface"""
        ## convert DOM namedNodeMap to SAX attributes
        nnm = n.attributes
        attrs = {}
        for a in nnm.values():
            attrs[a.nodeName] = a.value
        ## handle element
        name = n.nodeName
        self._cont_handler.startElement(name, AttributesImpl(attrs))
        self._from_dom(n.firstChild)

        self._cont_handler.endElement(name)


    def _element_ns(self, n):
        """ handle an ElementNode with NS interface"""
        ## convert DOM namedNodeMap to SAX attributes NS
        prefix_list = []
        nnm = n.attributes
        attrs, qnames = {}, {}
        for a in nnm.values():
            a_uri = a.namespaceURI
            if a_uri == XMLNS_NS:
                prefix, val = a.localName, a.value
                self._cont_handler.startPrefixMapping(prefix, val)
                prefix_list.append(prefix)
                if self._ns_prfx:
                    name = (a_uri, prefix)
                    attrs[name] = val
                    qnames[name] = a.nodeName
            else:
                name = (a_uri, a.localName)
                attrs[name] = a.value
                qnames[name] = a.nodeName
        ## handle element NS
        name = (n.namespaceURI, n.localName)
        self._cont_handler.startElementNS(name, n.nodeName,
                                          AttributesNSImpl(attrs, qnames))
        self._from_dom(n.firstChild)
        self._cont_handler.endElementNS(name, n.nodeName)
        prefix_list.reverse()
        map(self._cont_handler.endPrefixMapping, prefix_list)


## full sax handler, print each event to output ################################
class PrintSaxHandler:

    ## content handler #########################################################
    def setDocumentLocator(self, locator):
        print 'setDocumentLocator', locator
    def startDocument(self):
        print 'startDocument'
    def endDocument(self):
        print 'endDocument'
    def startElement(self, name, attrs):
        print 'startElement', name
        for key, val in attrs.items():
            print 'attribute', key,  val
    def endElement (self, name):
        print 'endElement', name
    def startElementNS(self, name, qname, attrs):
        print 'startElementNS', name, qname
        for key, val in attrs.items():
            print 'attribute', key,  val
    def endElementNS (self, name, qname):
        print 'endElementNS', name, qname
    def startPrefixMapping(self, prefix, uri):
        print 'startPrefixMapping', prefix, uri
    def endPrefixMapping(self, prefix):
        print 'endPrefixMapping', prefix
    def processingInstruction(self, target, data):
        print 'processingInstruction', target,  data
    def ignorableWhitespace(self, whitespace):
        print 'ignorableWhitespace', whitespace
    def characters(self, ch):
        print 'characters', ch.encode('iso-8859-15')

    ## lexical handler #########################################################
    def xmlDecl(self, version, encoding, standalone):
        print 'xmlDecl', version, encoding, standalone
    def comment(self, machin):
        print 'comment', machin.encode('UTF-8')
    def startEntity(self, name):
        print 'startEntity', name
    def endEntity(self, name):
        print 'endEntity', name
    def startCDATA(self):
        print 'startCDATA'
    def endCDATA(self):
        print 'endCDATA'
    def startDTD(self, name, public_id, system_id):
        print 'startDTD', name, public_id, system_id
    def endDTD(self):
        print 'endDTD'

    ## DTD decl handler ########################################################
    def attributeDecl(self, elem_name, attr_name, type, value_def, value):
        print 'attributeDecl', elem_name, attr_name, type, value_def, value
    def elementDecl(self, elem_name, content_model):
        print 'elementDecl', elem_name, content_model
    def internalEntityDecl(self, name, value):
        print 'internalEntityDecl', name, value.encode('UTF-8')
    def externalEntityDecl(self, name, public_id, system_id):
        print 'externalEntityDecl', name, public_id, system_id



# Test ########################################################################
def _parse(parser, doc, features, properties):
    import time
    h = PrintSaxHandler()
    parser.setContentHandler(h)
    print '-'*80
    print parser.__class__
    print
    for f,val in features:
        try:
            parser.setFeature(f, val)
            print f, val
        except Exception, e:
            print e
    for p, val in properties:
        try:
            if val:
                parser.setProperty(p, h)
            print p,val
        except Exception, e:
            print e
    print '*'*80
    t = time.time()
    parser.parse(doc)
    print '*'*80
    print 'TEMPS:', time.time() - t
    print
    
if __name__ == '__main__':
    import sys
    from xml.sax import make_parser
    from xml.dom.ext.reader import Sax2
    from xml.dom.ext import PrettyPrint
    from xml.sax.handler import feature_namespaces,\
         feature_namespace_prefixes, property_lexical_handler,\
         property_declaration_handler
    f1 = feature_namespaces
    f2 = feature_namespace_prefixes
    p1 = property_lexical_handler
    p2 = property_declaration_handler
    
    file = sys.argv[1]
    r = Sax2.Reader()
    f = open(file)
    doc = r.fromStream(f)
    print 'Initial document', doc, doc.__class__
    PrettyPrint(doc)
    for (val1,val2,val3,val4)  in ((0,0,0,0),(0,1,1,1),(1,0,0,0),(1,1,1,1)):
        for p,d in ((Dom2SaxParser(), doc),
                    (make_parser(['xml.sax.drivers2.drv_pyexpat']), f),
                    (make_parser(['xml.sax.drivers2.drv_xmlproc']), f)):
            if not d is doc:
                d = open(file)
            _parse(p, d, ((f1, val1), (f2,val2)), ((p1,val3),(p2,val4)))
            f.close()

