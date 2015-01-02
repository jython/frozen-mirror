########################################################################
#
# File Name:            HTMLDocument.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import Node
from xml.dom import NotSupportedErr

from xml.dom.Document import Document
from xml.dom import implementation
from xml.dom import ext

import string, sys

from xml.dom.html import HTML_DTD

class HTMLDocument(Document):

    def __init__(self):
        Document.__init__(self, None)
        # These only make sense in a browser environment, therefore
        # they never change
        self.__dict__['__referrer'] = ''
        self.__dict__['__domain'] = None
        self.__dict__['__URL'] = ''

        self.__dict__['__cookie'] = ''
        self.__dict__['__writable'] = 0
        self.__dict__['_html'] = vars(sys.modules['xml.dom.html'])

    ### Attribute Methods ###

    def _get_URL(self):
        return self.__dict__['__URL']

    def _get_anchors(self):
        anchors = self.getElementsByTagName('A');
        anchors = filter(lambda x: x._get_name(), anchors)
        return implementation._4dom_createHTMLCollection(anchors)

    def _get_applets(self):
        al = self.getElementsByTagName('APPLET')
        ol = self.getElementsByTagName('OBJECT')
        ol = filter(lambda x: x._get_code(), ol)
        return implementation._4dom_createHTMLCollection(al+ol)

    def _get_body(self):
        body = ''
        #Try to find the body or FRAMESET
        elements = self.getElementsByTagName('FRAMESET')
        if not elements:
            elements = self.getElementsByTagName('BODY')
        if elements:
            body = elements[0]
        else:
            #Create a body
            body = self.createElement('BODY')
            self.documentElement.appendChild(body)
        return body

    def _set_body(self, newBody):
        elements = self.getElementsByTagName('FRAMESET')
        if not elements:
            elements = self.getElementsByTagName('BODY')
        if elements:
            # Replace the existing one
            elements[0].parentNode.replaceChild(newBody, elements[0])
        else:
            # Add it
            self.documentElement.appendChild(newBody)

    def _get_cookie(self):
        return self.__dict__['__cookie']

    def _set_cookie(self, cookie):
        self.__dict__['__cookie'] = cookie

    def _get_domain(self):
        return self.__dict__['__domain']

    def _get_forms(self):
        forms = self.getElementsByTagName('FORM')
        return implementation._4dom_createHTMLCollection(forms)

    def _get_images(self):
        images = self.getElementsByTagName('IMG')
        return implementation._4dom_createHTMLCollection(images)

    def _get_links(self):
        areas = self.getElementsByTagName('AREA')
        anchors = self.getElementsByTagName('A')
        links = filter(lambda x: x._get_href(), areas+anchors)
        return implementation._4dom_createHTMLCollection(links)

    def _get_referrer(self):
        return self.__dict__['__referrer']

    def _get_title(self):
        elements = self.getElementsByTagName('TITLE')
        if elements:
            #Take the first
            title = elements[0]
            title.normalize()
            if title.firstChild:
                return title.firstChild.data
        return ''

    def _set_title(self, title):
        # See if we can find the title
        title_nodes = self.getElementsByTagName('TITLE')
        if title_nodes:
            title_node = title_nodes[0]
            title_node.normalize()
            if title_node.firstChild:
                title_node.firstChild.data = title
                return
        else:
            title_node = self.createElement('TITLE')
            self._4dom_getHead().appendChild(title_node)
        text = self.createTextNode(title)
        title_node.appendChild(text)

    ### Methods ###

    def close(self):
        self.__dict__['__writable'] = 0

    def getElementsByName(self, elementName):
        return self._4dom_getElementsByAttribute('*', 'NAME', elementName)

    def open(self):
        #Clear out the doc
        self.__dict__['__referrer'] = ''
        self.__dict__['__domain'] = None
        self.__dict__['__url'] = ''
        self.__dict__['__cookie'] = ''
        self.__dict__['__writable'] = 1

    def write(self, st):
        if not self.__dict__['__writable']:
            return
        #We need to parse the string here
        from xml.dom.ext.reader.HtmlLib import FromHTML
        d = FromHtml(st, self)
        if d != self:
            self.appendChild(d)

    def writeln(self, st):
        st = st + '\n'
        self.write(st)


    def getElementByID(self, ID):
        hc = self._4dom_getElementsByAttribute('*','ID',ID)
        if hc.length != 0:
            return hc[0]
        return None

    ### Overridden Methods ###

    def createElement(self, tagName):
        return self._4dom_createHTMLElement(tagName)

    def createElementNS(self, namespace, qname):
        return self._4dom_createHTMLElement(qname)

    def createAttribute(self, name):
        return Document.createAttribute(self, string.upper(name))

    def createCDATASection(*args, **kw):
        raise NotSupportedErr()

    def createEntityReference(*args, **kw):
        raise NotSupportedErr()

    def createProcessingInstruction(*args, **kw):
        raise NotSupportedErr()

    def _4dom_createEntity(*args, **kw):
        raise NotSupportedErr()

    def _4dom_createNotation(*args, **kw):
        raise NotSupportedErr()

    ### Internal Methods ###

    def _4dom_getElementsByAttribute(self, tagName, attribute, attrValue=None):
        nl = self.getElementsByTagName(tagName)
        hc = implementation._4dom_createHTMLCollection()
        for elem in nl:
            attr = elem.getAttribute(attribute)
            if attrValue == None and attr != '':
                hc.append(elem)
            elif attr == attrValue:
                hc.append(elem)
        return hc

    def _4dom_getHead(self):
        nl = self.getElementsByTagName('HEAD')
        if not nl:
            head = self.createElement('HEAD')
            #The head goes in front of the body
            body = self._get_body()
            self.documentElement.insertBefore(head, body)
        else:
            head = nl[0]
        return head

    def _4dom_createHTMLElement(self, tagName):
        lowered = string.lower(tagName)
        if not HTML_DTD.has_key(lowered):
            raise TypeError('Unknown HTML Element: %s' % tagName)

        if lowered in NoClassTags:
            from HTMLElement import HTMLElement
            return HTMLElement(self, tagName)

        #FIXME: capitalize() broken with unicode in Python 2.0
        #normTagName = string.capitalize(tagName)
        capitalized = string.upper(tagName[0]) + lowered[1:]
        element = HTMLTagMap.get(capitalized, capitalized)
        module = 'HTML%sElement' % element
        if not self._html.has_key(module):
            #Try to import it (should never fail)
            __import__('xml.dom.html.%s' % module)
        # Class and module have the same name
        klass = getattr(self._html[module], module)
        return klass(self, tagName)

    def cloneNode(self, deep):
        clone = HTMLDocument()
        clone.__dict__['__referrer'] = self._get_referrer()
        clone.__dict__['__domain'] = self._get_domain()
        clone.__dict__['__URL'] = self._get_URL()
        clone.__dict__['__cookie'] = self._get_cookie()
        if deep:
            if self.doctype is not None:
                # Cannot have any children, no deep needed
                dt = self.doctype.cloneNode(0)
                clone._4dom_setDocumentType(dt)
            if self.documentElement is not None:
                # The root element can have children, duh
                root = self.documentElement.cloneNode(1, newOwner=clone)
                clone.appendChild(root)
        return clone

    def isXml(self):
        return 0

    def isHtml(self):
        return 1

    ### Attribute Access Mappings ###

    _readComputedAttrs = Document._readComputedAttrs.copy()
    _readComputedAttrs.update ({
         'title'         : _get_title,
         'referrer'      : _get_referrer,
         'domain'        : _get_domain,
         'URL'           : _get_URL,
         'body'          : _get_body,
         'images'        : _get_images,
         'applets'       : _get_applets,
         'links'         : _get_links,
         'forms'         : _get_forms,
         'anchors'       : _get_anchors,
         'cookie'        : _get_cookie
      })

    _writeComputedAttrs = Document._writeComputedAttrs.copy()
    _writeComputedAttrs.update ({
         'title'         : _set_title,
         'body'          : _set_body,
         'cookie'        : _set_cookie,
      })

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            Document._readOnlyAttrs + _readComputedAttrs.keys())

# HTML tags that don't map directly to a class name
HTMLTagMap =    {'Isindex':     'IsIndex',
                 'Optgroup':    'OptGroup',
                 'Textarea':    'TextArea',
                 'Fieldset':    'FieldSet',
                 'Ul':          'UList',
                 'Ol':          'OList',
                 'Dl':          'DList',
                 'Dir':         'Directory',
                 'Li':          'LI',
                 'P':           'Paragraph',
                 'H1':          'Heading',
                 'H2':          'Heading',
                 'H3':          'Heading',
                 'H4':          'Heading',
                 'H5':          'Heading',
                 'H6':          'Heading',
                 'Q':           'Quote',
                 'Blockquote':  'Quote',
                 'Br':          'BR',
                 'Basefont':    'BaseFont',
                 'Hr':          'HR',
                 'A':           'Anchor',
                 'Img':         'Image',
                 'Caption':     'TableCaption',
                 'Col':         'TableCol',
                 'Colgroup':    'TableCol',
                 'Td':          'TableCell',
                 'Th':          'TableCell',
                 'Tr':          'TableRow',
                 'Thead':       'TableSection',
                 'Tbody':       'TableSection',
                 'Tfoot':       'TableSection',
                 'Frameset':    'FrameSet',
                 'Iframe':      'IFrame',
                 'Form':        'Form',
                 'Ins' :        'Mod',
                 'Del' :        'Mod',
                }

#HTML Elements with no specific DOM Interface of their own
NoClassTags =   ['sub',
                 'sup',
                 'span',
                 'bdo',
                 'tt',
                 'i',
                 'b',
                 'u',
                 's',
                 'strike',
                 'big',
                 'small',
                 'em',
                 'strong',
                 'dfn',
                 'code',
                 'samp',
                 'kbd',
                 'var',
                 'cite',
                 'acronym',
                 'abbr',
                 'dd',
                 'dt',
                 'noframes',
                 'noscript',
                 'address',
                 'center',
                 ]
