import string
import Printer
from xml.dom import XHTML_NAMESPACE

# Wrapper classes to convert nodes from HTML to XHTML

class XHtmlDocType:
    def __init__(self, doctype):
        self.name = 'html'
        self.publicId = "-//W3C//DTD XHTML 1.0 Strict//EN"
        self.systemId = "DTD/xhtml1-strict.dtd"
        self.entities = doctype and doctype.entities or []
        self.notations = doctype and doctype.notation or []
        return

class XHtmlAttr:
    def __init__(self, node):
        self.namespaceURI = XHTML_NAMESPACE
        self.name = string.lower(node.name)
        self.node = node
        return

    def __getattr__(self, key):
        return getattr(self.node, key)

class XHtmlElement:
    def __init__(self, node):
        self.tagName = string.lower(node.tagName)
        self.node = node
        return

    def __getattr__(self, key):
        return getattr(self.node, key)

class XHtmlPrintVisitor(Printer.PrintVisitor):
    def __init__(self, stream, encoding, indent):
        xhtml = {None: 'http://www.w3.org/1999/xhtml'}
        Printer.PrintVisitor.__init__(self, stream, encoding, indent, nsHints=xhtml)
        self._html = 0
        return

    def visitDocument(self,node):
        self.visitProlog()
        self._tryIndent()
        self.visitDocumentType(XHtmlDocType(node.doctype))
        self.visitNodeList(node.childNodes, exclude=node.doctype)
        return

    def visitAttr(self, node):
        Printer.PrintVisitor.visitAttr(self, XHtmlAttr(node))
        return

    def visitElement(self, node):
        Printer.PrintVisitor.visitElement(self, XHtmlElement(node))
        return
