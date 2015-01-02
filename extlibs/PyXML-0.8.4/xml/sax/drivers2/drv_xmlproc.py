"""
A SAX 2.0 driver for xmlproc.

$Id: drv_xmlproc.py,v 1.16 2003/07/27 17:58:20 loewis Exp $
"""

import types, string

from xml.parsers.xmlproc import xmlproc, xmlval, xmlapp
from xml.sax import saxlib
from xml.sax.xmlreader import AttributesImpl, AttributesNSImpl
from xml.sax.xmlreader import IncrementalParser
from xml.sax.saxutils import ContentGenerator, prepare_input_source

# Todo
# - EntityResolver InputSource handling
# - as much as possible of LexicalHandler
# - entity expansion features
# - core properties
# - extra properties/features
#   - element stack
#   - entity stack
#   - current error code
#   - byte offset
#   - DTD object
#   - catalog path
#   - use catalogs
# - regression test
# - methods from Python SAX extensions?
# - remove FIXMEs

class XmlprocDriver(IncrementalParser):

    # ===== SAX 2.0 INTERFACES

    # --- XMLReader methods

    def __init__(self):
        IncrementalParser.__init__(self)
        self.__parsing = 0
        self.__validate = 0
        self.__namespaces = 0
        self.__ext_pes = 0

        self.__locator = 0

        self._lex_handler = saxlib.LexicalHandler()
        self._decl_handler = saxlib.DeclHandler()
        self._parser = None

    def prepareParser(self, source):
        self.__parsing = 1

        # create parser

        if self.__validate:
            parser = xmlval.XMLValidator()
        else:
            parser = xmlproc.XMLProcessor()

        # set handlers

        if self._cont_handler != None or self._lex_handler != None:
            if self._cont_handler == None:
                self._cont_handler = saxlib.ContentHandler()
            if self._lex_handler == None:
                self._lex_handler = saxlib.LexicalHandler()

            if self.__namespaces:
                filter = NamespaceFilter(parser, self._cont_handler,
                                         self._lex_handler, self)
                parser.set_application(filter)
            else:
                parser.set_application(self)

        if self._err_handler != None:
            parser.set_error_handler(self)

        if self._decl_handler != None or self._dtd_handler != None:
            parser.set_dtd_listener(self)

        parser.set_pubid_resolver(self)
        
        # FIXME: set other handlers

        if self.__ext_pes:
            parser.set_read_external_subset(1)

        self._parser = parser # make it available for callbacks
        if source:
            parser.set_sysid(source.getSystemId())

    def feed(self, data):
        if not self._parser:
            self.prepareParser(None)
        self._parser.feed(data)

    def close(self):
        self._parser.flush()
        self._parser.parseEnd()

    def reset(self):
        self._parser = None
        self.__parsing = 0

    def setLocale(self, locale):
        pass

    def getFeature(self, name):
        if name == saxlib.feature_string_interning or \
           name == saxlib.feature_external_ges:
            return 1
        elif name == saxlib.feature_external_pes:
            return self.__ext_pes
        elif name == saxlib.feature_validation:
            return self.__validate
        elif name == saxlib.feature_namespaces:
            return self.__namespaces
        elif name == saxlib.feature_namespace_prefixes:
            return 0
        else:
            raise saxlib.SAXNotRecognizedException("Feature '%s' not recognized" %
                                            name)

    def setFeature(self, name, state):
        if self.__parsing:
            raise saxlib.SAXNotSupportedException("Cannot set feature '%s' during parsing" % name)

        if name == saxlib.feature_validation:
            self.__validate = state
            if self.__validate:
                self.__ext_pes = 1
        elif name == saxlib.feature_namespaces:
            self.__namespaces = state
        elif name == saxlib.feature_external_ges or \
             name == saxlib.feature_string_interning:
            if not state:
                raise saxlib.SAXNotSupportedException("This feature cannot be turned off with xmlproc.")
        elif name == saxlib.feature_namespace_prefixes:
            if state:
                raise saxlib.SAXNotSupportedException("This feature cannot be turned on with xmlproc.")
        elif name == saxlib.feature_external_pes:
            self.__ext_pes = state
        else:
            raise saxlib.SAXNotRecognizedException("Feature '%s' not recognized" %
                                            name)

    def getProperty(self, name):
        if name == saxlib.property_lexical_handler:
            return self._lex_handler
        elif name == saxlib.property_declaration_handler:
            return self._decl_handler

        raise saxlib.SAXNotRecognizedException("Property '%s' not recognized" % name)

    def setProperty(self, name, value):
        if name == saxlib.property_lexical_handler:
            self._lex_handler = value
        elif name == saxlib.property_declaration_handler:
            self._decl_handler = value
        else:
            raise saxlib.SAXNotRecognizedException("Property '%s' not recognized" % name)

    # --- Locator methods

    def getColumnNumber(self):
        return self._parser.get_column()

    def getLineNumber(self):
        return self._parser.get_line()

    def getPublicId(self):
        return None  # FIXME: Try to find this. Perhaps from InputSource?

    def getSystemId(self):
        return self._parser.get_current_sysid() # FIXME?

    # ===== XMLPROC INTERFACES

    # --- Application methods

    def set_locator(self, locator):
        self._locator = locator

    def doc_start(self):
        self._cont_handler.startDocument()

    def doc_end(self):
        self._cont_handler.endDocument()

    def handle_comment(self, data):
        self._lex_handler.comment(data)

    def handle_start_tag(self, name, attrs):
        self._cont_handler.startElement(name, AttributesImpl(attrs))

    def handle_end_tag(self,name):
        self._cont_handler.endElement(name)

    def handle_data(self, data, start, end):
        self._cont_handler.characters(data[start:end])

    def handle_ignorable_data(self, data, start, end):
        self._cont_handler.ignorableWhitespace(data[start:end])

    def handle_pi(self, target, data):
        self._cont_handler.processingInstruction(target, data)

    def handle_doctype(self, root, pubId, sysId):
        self._lex_handler.startDTD(root, pubId, sysId)

    def set_entity_info(self, xmlver, enc, sddecl):
        pass

    # --- ErrorHandler methods

    # set_locator implemented as Application method above

    def get_locator(self):
        return self._locator

    def warning(self, msg):
        self._err_handler.warning(saxlib.SAXParseException(msg, None, self))

    def error(self, msg):
        self._err_handler.error(saxlib.SAXParseException(msg, None, self))

    def fatal(self, msg):
        self._err_handler.fatalError(saxlib.SAXParseException(msg, None, self))

    # --- DTDConsumer methods

    def dtd_start(self):
        pass # this is done by handle_doctype

    def dtd_end(self):

        self._lex_handler.endDTD()

    def handle_comment(self, contents):
        self._lex_handler.comment(contents)

    def handle_pi(self, target, rem):
        self._cont_handler.processingInstruction(target, rem)

    def new_general_entity(self, name, val):
        self._decl_handler.internalEntityDecl(name, val)

    def new_external_entity(self, ent_name, pub_id, sys_id, ndata):
        if not ndata:
            self._decl_handler.externalEntityDecl(ent_name, pub_id, sys_id)
        else:
            self._dtd_handler.unparsedEntityDecl(ent_name, pub_id, sys_id,
                                                 ndata)

    def new_parameter_entity(self, name, val):
        self._decl_handler.internalEntityDecl("%" + name, val)

    def new_external_pe(self, name, pubid, sysid):
        self._decl_handler.externalEntityDecl("%" + name, pubid, sysid)

    def new_notation(self, name, pubid, sysid):
        self._dtd_handler.notationDecl(name, pubid, sysid)

    def new_element_type(self, elem_name, elem_cont):
        if elem_cont == None:
            elem_cont = "ANY"
        elif elem_cont == ("", [], ""):
            elem_cont = "EMPTY"
        self._decl_handler.elementDecl(elem_name, elem_cont)

    def new_attribute(self, elem, attr, type, a_decl, a_def):
        self._decl_handler.attributeDecl(elem, attr, type, a_decl, a_def)

    # --- PubIdResolver methods

    def resolve_pe_pubid(self, pubid, sysid):
        # Delegate out to the instance's EntityResolver.
        # TODO: does not support returning an InputSource from resolveEntity.
        return self._ent_handler.resolveEntity(pubid, sysid)
    
    def resolve_doctype_pubid(self, pubid, sysid):
        # Delegate out to the instance's EntityResolver.
        # TODO: does not support returning an InputSource from resolveEntity.
        return self._ent_handler.resolveEntity(pubid, sysid)
    
    def resolve_entity_pubid(self, pubid, sysid):
        # Delegate out to the instance's EntityResolver.
        # TODO: does not support returning an InputSource from resolveEntity.
        return self._ent_handler.resolveEntity(pubid, sysid)

# --- NamespaceFilter

class NamespaceFilter:
    """An xmlproc application that processes qualified names and reports them
    as (URI, local-part). It reports errors through the error reporting
    mechanisms of the parser."""

    def __init__(self, parser, content, lexical, driver):
        self._cont_handler = content
        self._lex_handler = lexical
        self.driver = driver
        self.ns_map = {"" : None} # Current prefix -> URI map
        self.ns_map["xml"] = "http://www.w3.org/XML/1998/namespace"
        self.ns_stack = []     # Pushed for each element, used to maint ns_map
        self.rep_ns_attrs = 0  # Report xmlns-attributes?
        self.parser = parser

    def set_locator(self, locator):
        self.driver.set_locator(locator)

    def doc_start(self):
        self._cont_handler.startDocument()

    def doc_end(self):
        self._cont_handler.endDocument()

    def handle_comment(self, data):
        self._lex_handler.comment(data)

    def handle_start_tag(self,name,attrs):
        old_ns={} # Reset ns_map to these values when we leave this element
        del_ns=[] # Delete these prefixes from ns_map when we leave element

        # attrs=attrs.copy()   Will have to do this if more filters are made

        # Find declarations, update self.ns_map and self.ns_stack
        for (a,v) in attrs.items():
            if a[:6]=="xmlns:":
                prefix=a[6:]
                if string.find(prefix,":")!=-1:
                    self.parser.report_error(1900)

                #if v=="":
                #    self.parser.report_error(1901)
            elif a=="xmlns":
                prefix=""
            else:
                continue

            if self.ns_map.has_key(prefix):
                old_ns[prefix]=self.ns_map[prefix]
            if v:
                self.ns_map[prefix]=v
            else:
                del self.ns_map[prefix]

            if not self.rep_ns_attrs:
                del attrs[a]

        self.ns_stack.append((old_ns,del_ns))

        # Process elem and attr names
        cooked_name = self.__process_name(name)
        ns = cooked_name[0]

        rawnames = {}
        for (a,v) in attrs.items():
            del attrs[a]
            aname = self.__process_name(a, is_attr=1)
            if attrs.has_key(aname):
                self.parser.report_error(1903)
            attrs[aname] = v
            rawnames[aname] = a

        # Report event
        self._cont_handler.startElementNS(cooked_name, name,
                                          AttributesNSImpl(attrs, rawnames))

    def handle_end_tag(self, rawname):
        name = self.__process_name(rawname)

        # Clean up self.ns_map and self.ns_stack
        (old_ns,del_ns)=self.ns_stack[-1]
        del self.ns_stack[-1]

        self.ns_map.update(old_ns)
        for prefix in del_ns:
            del self.ns_map[prefix]

        self._cont_handler.endElementNS(name, rawname)

    def handle_data(self, data, start, end):
        self._cont_handler.characters(data[start:end])

    def handle_ignorable_data(self, data, start, end):
        self._cont_handler.ignorableWhitespace(data[start:end])

    def handle_pi(self, target, data):
        self._cont_handler.processingInstruction(target, data)

    def handle_doctype(self, root, pubId, sysId):
        self._lex_handler.startDTD(root, pubId, sysId)

    def set_entity_info(self, xmlver, enc, sddecl):
        pass

    # --- Internal methods

    def __process_name(self, name, default_to=None, is_attr=0):
        n=string.split(name,":")
        if len(n)>2:
            self.parser.report_error(1900)
            return (None, name)
        elif len(n)==2:
            if n[0]=="xmlns":
                return (None, name)

            try:
                return (self.ns_map[n[0]], n[1])
            except KeyError:
                self.parser.report_error(1902)
                return (None, name)
        elif is_attr:
            return (None, name)
        elif default_to != None:
            return (default_to, name)
        elif self.ns_map.has_key("") and name != "xmlns":
            return (self.ns_map[""],name)
        else:
            return (None, name)

def create_parser():
    return XmlprocDriver()
