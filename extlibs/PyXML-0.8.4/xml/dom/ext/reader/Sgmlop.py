import string, re, types, sys
from xml.parsers import sgmlop
from xml.dom import implementation
from xml.dom import Node
from xml.dom import NotSupportedErr
from xml.dom import EMPTY_NAMESPACE
from xml.dom.html import HTML_DTD, HTML_CHARACTER_ENTITIES

DEFAULT_CHARSET = 'ISO-8859-1'

_root = '(?P<root>[a-zA-Z][a-zA-Z0-9]*)'
_quoted = '("[^"]*")|' + "('[^']*')"
_sysId = r'\s*(?P<system%d>' + _quoted + ')'
_pubId = r'\s*PUBLIC\s*(?P<public>' + _quoted + '(' + (_sysId % 1) + ')?)'
_sysId = 'SYSTEM' + (_sysId % 2)
_doctype = re.compile('DOCTYPE ' + _root + '(%s|%s)?' % (_pubId, _sysId), re.I)

try:
    unicode()
except:
    from xml.unicode.iso8859 import wstring
    wstring.install_alias('ISO-8859-1', 'ISO_8859-1:1987')

    def unicode(str, encoding='US-ASCII'):
        """Create a UTF-8 string"""
        try:
            return wstring.decode(string.upper(encoding), str).utf8()
        except:
            return str

    def unichr(char):
        """Create a UTF-8 string from a Unicode character code"""
        try:
            return wstring.chr(char).utf8()
        except:
            return char

class SgmlopParser:
    def __init__(self, entities=None):
        self.entities = {'amp' : '&',
                         'apos' : "'",
                         'lt' : '<',
                         'gt' : '>',
                         'quot' : '"',
                         }
        entities and self.entities.update(entities)

    def initParser(self, parser):
        self._parser = parser
        self._parser.register(self)
        return

    def initState(self, ownerDoc=None):
        raise NotImplementError('initState: ownerDoc=%s' % ownerDoc)

    def parse(self, stream):
        self._parser.parse(stream.read())
        return

    def handle_special(self, data):
        """Handles <!...> directives"""
        raise NotImplementedError('handle_special: data=%s' % data)

    def handle_proc(self, target, data):
        """Handles processing instructions."""
        raise NotImplementedError('handle_proc: target=%s, data=%s' % (target, data))

    def finish_starttag(self, tagname, attrs):
        """
        In XML mode attrs is a dictionary, otherwise a list.
        """
        raise NotImplementedError('finish_starttag: name=%s' % tagname)

    def finish_endtag(self, tagname):
        raise NotImplementedError('finish_endtag: name=%s' % tagname)

    def handle_entityref(self, name):
        if self.entities.has_key(name):
            self.handle_data(self.entities[name])
        else:
            self.unknown_entityref(name)
        return

    #Handled internally in sgmlop, but can be overridden
    #def handle_charref(self, char):
    #    # char is a string number
    #    # either DDD or xHHH
    #    if char[0] == 'x':
    #        self.handle_data(chr(eval('0' + char)))
    #    else:
    #        self.handle_data(chr(int(char)))
    #    return

    def handle_cdata(self, data):
        raise NotImplementedError('handle_cdata: data=%s' % data)

    def handle_data(self, data):
        raise NotImplementedError('handle_data: data=%s' % data)

    def handle_comment(self, data):
        raise NotImplementedError('handle_comment: data=%s' % data)

    def unknown_endtag(self, name): pass
    def unknown_entityref(self, name): pass

g_reCharset = re.compile(r'charset\s*=\s*(?P<charset>[a-zA-Z0-9_\-]+)')

HTML_ENTITIES = {}
for (char, name) in HTML_CHARACTER_ENTITIES.items():
    HTML_ENTITIES[name] = unichr(char)

class HtmlParser(SgmlopParser):

    def __init__(self):
        SgmlopParser.__init__(self, HTML_ENTITIES)

    def initParser(self):
        SgmlopParser.initParser(self, sgmlop.SGMLParser())

    def initState(self, ownerDoc=None, charset=''):
        self._ownerDoc = ownerDoc or implementation.createHTMLDocument('')
        self._charset = charset or DEFAULT_CHARSET
        self.rootNode = self._ownerDoc.createDocumentFragment()
        self._stack = [self.rootNode]
        self._hasHtml = 0
        return

    def handle_special(self, data):
        # This would be a doctype, but HTML DOMs do not use them
        return

    def handle_proc(self, target, data):
        # HTML DOMs do not support processing instructions either.
        return

    def finish_starttag(self, tagname, attrs):
        unicodeTagName = unicode(tagname, self._charset)
        lowerTagName = string.lower(unicodeTagName)
        if not HTML_DTD.has_key(lowerTagName):
            # Skip any tags not defined in HTML 4.01
            return

        element = self._ownerDoc.createElementNS(EMPTY_NAMESPACE, unicodeTagName)

        # Allows for multiple META tags in a document
        if lowerTagName == 'meta':
            lowered = map(lambda (name, value):
                          (string.lower(name), string.lower(value)),
                          attrs)
            if ('http-equiv', 'content-type') in lowered:
                for (name, value) in lowered:
                    if name == 'content':
                        match = g_reCharset.search(value)
                        if match:
                            self._charset = match.group('charset')

        # Add any attributes to the tag
        for (name, value) in attrs:
            element.setAttributeNS(EMPTY_NAMESPACE, unicode(name, self._charset),
                                   unicode(value, self._charset))

        # Look for its parent
        for i in range(1, len(self._stack)):
            parent = self._stack[-i]
            if lowerTagName in HTML_DTD[string.lower(parent.tagName)]:
                parent.appendChild(element)
                if i > 1:
                    self._stack = self._stack[:-i+1]
                if HTML_DTD[lowerTagName]:
                    self._stack.append(element)
                return

        # no parent found
        if not self._hasHtml and lowerTagName == 'html':
            self._stack[0].appendChild(element)
            self._stack.append(element)
            self._hasHtml = 1
        return

    def finish_endtag(self, tagname):
        uppercase = string.upper(unicode(tagname, self._charset))
        # Look for opening tag
        for i in range(1, len(self._stack)):
            element = self._stack[-i]
            if uppercase == element.tagName:
                self._stack = self._stack[:-i]
                break
        return

    def handle_entityref(self, name):
        if self.entities.has_key(name):
            unidata = self.entities[name]
            node = self._stack[-1]
            text_node = node.lastChild or node
            if text_node.nodeType == Node.TEXT_NODE:
                text_node.appendData(unidata)
            else:
                node.appendChild(self._ownerDoc.createTextNode(unidata))
        else:
            self.unknown_entityref(name)
        return

    def handle_data(self, data):
        unidata = unicode(data, self._charset)
        node = self._stack[-1]
        text_node = node.lastChild or node
        if text_node.nodeType == Node.TEXT_NODE:
            text_node.appendData(unidata)
        else:
            node.appendChild(self._ownerDoc.createTextNode(unidata))
        return

    def handle_charref(self, value):
        # Can't rely on sgmlop to handle charrefs itself: it can't
        # report Unicode (since it won't know the document encoding),
        # and it may encounter non-ASCII characters

        if value[0] == 'x':
            value = int(value[1:], 16)
        else:
            value = int(value)
        
        unidata = unichr(value)
        node = self._stack[-1]
        text_node = node.lastChild or node
        if text_node.nodeType == Node.TEXT_NODE:
            text_node.appendData(unidata)
        else:
            node.appendChild(self._ownerDoc.createTextNode(unidata))
        return

    def handle_comment(self, data):
        comment = self._ownerDoc.createComment(data)
        self._stack[-1].appendChild(comment)
        return

class XmlParser(SgmlopParser):

    def initParser(self):
        SgmlopParser.initParser(self, sgmlop.XMLParser())

    def initState(self, ownerDoc=None):
        self._ownerDoc = None
        #Set up the stack which keeps track of the nesting of DOM nodes.
        if ownerDoc:
            self._ownerDoc = ownerDoc
            #Create a docfrag to hold all the generated nodes.
            self._rootNode = self._ownerDoc.createDocumentFragment()
            self._stack = [self._rootNode]
        else:
            self._rootNode = None
            self._stack = []
        self._dt = None
        self._xmlDecl = None
        self._orphanedNodes = []
        self._namespaces = {'xml': XML_NAMESPACE}
        self._namespaceStack = []
        self._currText = ''
        return

    def finish_starttag(self, tagname, attrs):
        old_nss = {}
        del_nss = []
        split_attrs = {}
        for (name, value) in attrs.items():
            (prefix, local) = SplitQName(name)
            split_attrs[(prefix, local, name)] = value
            if local == 'xmlns':
                if self._namespaces.has_key(prefix):
                    old_nss[prefix] = self._namespaces[prefix]
                else:
                    del_nss.append(prefix)
                if prefix or value:
                    self._namespaces[prefix] = value
                else:
                    del_nss.append(prefix)
        self._namespaceStack.append((old_nss, del_nss))

        (prefix, local) = SplitQName(tagname)
        namespace = self._namespaces.get(prefix, None)
        element = self._ownerDoc.createElementNS(namespace, tagname)
        for ((prefix, local, name), value) in split_attrs.items():
            if local == 'xmlns':
                namespace = XMLNS_NAMESPACE
            else:
                namespace = self._namespaces.get(prefix, None)
            attr = self._ownerDoc.createAttributeNS(namespace, name)
            attr.value = value
            element.setAttributeNodeNS(attr)

        self._stack.append(element)

    def finish_endtag(self, tagname):
        element = self._stack.pop()
        (old_nss, del_nss) = self._namespaceStack.pop()
        self._namespaces.update(old_nss)
        for prefix in del_nss:
            del self._namespaces[prefix]
        self._stack[-1].appendChild(element)
        return
