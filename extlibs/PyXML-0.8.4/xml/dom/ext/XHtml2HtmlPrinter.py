import string
import Printer
from xml.dom import XHTML_NAMESPACE
from xml.dom.html import HTML_FORBIDDEN_END

class HtmlDocType:
    name = 'HTML'
    publicId = "-//W3C//DTD HTML 4.0//EN"
    systemId = "http://www.w3.org/TR/REC-html40/strict.dtd"
    entities = notations = []

class HtmlAttr:
    def __init__(self, node):
        self.namespaceURI = None
        self.name = string.upper(node.localName or node.nodeName)
        self.value = node.value
        return

class HtmlElement:
    def __init__(self, node):
        self.tagName = string.upper(node.localName or node.nodeName)
        self.childNodes = node.childNodes
        self.attributes = node.attributes
        return

class XHtml2HtmlPrintVisitor(Printer.PrintVisitor):
    def __init__(self, stream, encoding, indent='', plainElements=None):
        Printer.PrintVisitor.__init__(self,stream,encoding,indent,plainElements)
        self._html = 1
        return

    def visitDocument(self, doc):
        self.visitDocumentType(HtmlDocType)
        self.visitNodeList(doc.childNodes, exclude=doc.doctype)
        return

    def visitAttr(self, node):
        if node.namespaceURI and node.namespaceURI != XHTML_NAMESPACE:
            return
        Printer.PrintVisitor.visitAttr(self,HtmlAttr(node))

    def visitElement(self, node):
        if node.namespaceURI and node.namespaceURI != XHTML_NAMESPACE:
            return
        htmlElement = HtmlElement(node)
        if htmlElement.tagName == 'XHTML':
            htmlElement.tagName = 'HTML'
        Printer.PrintVisitor.visitElement(self,htmlElement)
