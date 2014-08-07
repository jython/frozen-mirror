# PyTREX: A clean-room implementation of TREX in Python
# by James Tauber
#
# http://pytrex.sourceforge.net/
#
# Copyright (c) 2001, James Tauber
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
# * The name "James Tauber" may not be used to endorse or promote
#   products derived from this software without specific prior written
#   permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


########################################################################
#
# TO USE FROM THE COMMAND LINE:
# - python pytrex.py <trex-file> <instance-file>
#
# TO USE IN OTHER PYTHON SCRIPTS:
# - import the pytrex.py file (must be on PYTHONPATH):
#     from pytrex import *
# - parse the TREX file:
#     trex = parse_TREX("foo.trex")
# - parse the instance file:
#     instance = parse_Instance("bar.xml")
# - validate
#     match = validate(trex, instance)
#   match will be an Error object if invalid - test with isError()
#
# You can see an internal representation of the TREX grammar and the
# instance with trex.display() and instance.display() respectively
#
# You can also see a representation of the match object returned by
# validate with match.display()
#
# NOT IMPLEMENTED YET
# - ns attribute inheritance that takes into account inclusion
# - anonymous datatypes
#
# questions:
#
# zeroOrMore = empty | oneOrMore
# but empty doesn't allow whitespace and zeroOrMore does
#
# DATATYPE SUPPORT
#
# PyTREX has support for named datatypes in general but none in
# particular. To add support for a particular datatype, write a
# function (or lambda) that takes a string and returns 1 or 0
# depending on whether the datatype allows the given string as a
# lexical representation. Then register the datatype by calling: 
#
#   register_datatype(<namespaceURI of datatype>, <NCName of datatype>,
#                     <test function>)



########################################################################
### COMMON

class HandlerBase:
    def __init__(self, parser, parent, atts):
        self.parser = parser
        self.parent = parent
        if self.parent != None:
            self.ns_decls = self.parent.ns_decls
        else:
            self.ns_decls = {}
        self.set_handlers()

    def set_handlers(self):
        self.parser.StartElementHandler = self.child
        self.parser.CharacterDataHandler = self.char
        self.parser.EndElementHandler = self.end
        self.parser.StartNamespaceDeclHandler = self.start_ns_decl
        self.parser.EndNamespaceDeclHandler = self.end_ns_decl

    def start_ns_decl(self, prefix, uri):
        self.ns_decls[prefix] = uri

    def end_ns_decl(self, prefix):
        del self.ns_decls[prefix]

    def child(self, name, atts):
        pass

    def char(self, data):
        pass

    def child(self, name, atts):
        pass
    
    def end(self, name):
        if self.parent != None:
            self.parent.set_handlers()
        else: # must be root
            pass



########################################################################
### TREX PARSING

trex_ns = "http://www.thaiopensource.com/trex"

def parse_TREX(location, baseURI=None):
    if baseURI==None:
        baseURI = location

    import xml.parsers.expat
    parser = xml.parsers.expat.ParserCreate(namespace_separator="^")
    parser.SetBase(baseURI)
    parser.returns_unicode = 1

    r = T_RootHandler(parser)

    from urllib2 import urlopen
    # TODO: doesn't catch well-formedness errors in TREX
    try:
        f = urlopen(location)
        parser.ParseFile(f)
    except IOError, e:
        print "IOError reading TREX file", e
        import sys; sys.exit()
    except xml.parsers.expat.error:
        print "Error parsing file at line '%s' and column '%s'\n" % (parser.ErrorLineNumber, parser.ErrorColumnNumber)
        f.close()
        import sys; sys.exit()
    except TREXError, e:
        print "Error parsing TREX file:", e.value
        f.close()
        import sys; sys.exit()
    f.close()

    return r.product


class TREXError:
    def __init__(self, value):
        self.value = value


class T_HandlerBase(HandlerBase):
    def __init__(self, parser, parent, atts):
        HandlerBase.__init__(self, parser, parent, atts)
        if atts != None:
            if atts.has_key("ns"):
                self.ns_attr = atts["ns"]
            else: 
                self.ns_attr = parent.ns_attr
        else: # must be root
            self.ns_attr = ""
        if parent != None:
            self.using_trex_ns = parent.using_trex_ns

    # handle children of elements that can take pattern children
    def child_pattern(self, name, atts):
        if not handlePattern(self.parser, self, name, atts):
            if in_trex_ns(name):
                raise TREXError, "%s not allowed here" % name
            elif not self.using_trex_ns and in_default_ns(name):
                raise TREXError, "%s not allowed here" % name
            else:
                T_Ignore(self.parser, self, name, atts)

    # handle children of elements that take name-class
    def child_nameclass(self, name, atts):
        if not handleNameClass(self.parser, self, name, atts):
            if in_trex_ns(name):
                raise TREXError, "%s not allowed here" % name
            elif not self.using_trex_ns and in_default_ns(name):
                raise TREXError, "%s not allowed here" % name
            else:
                T_Ignore(self.parser, self, name, atts)

    # handle children of elements that take name-class and patterns
    def child_nameclass_pattern(self, name, atts):
        if self.product.name_class==None:
            self.child_nameclass(name, atts)
        else:
            self.child_pattern(name, atts)

    # handle children of elements that take no children
    def child_none(self, name, atts):
        raise TREXError, "%s not allowed here" % name

    # handler children of elements that can only take non-trex children
    def child_non_trex(self, name, atts):
        if in_trex_ns(name):
            raise TREXError, "%s not allowed here" % ncname
        elif not self.using_trex_ns and in_default_ns(name):
            raise TREXError, "%s not allowed here" % ncname
        else:
            T_Ignore(self.parser, self, name, atts)


class T_Ignore(T_HandlerBase):
    def __init__(self, parser, parent, name, atts):
        T_HandlerBase.__init__(self, parser, parent, None)

    child = T_HandlerBase.child_non_trex


class T_RootHandler(T_HandlerBase):
    def __init__(self, parser, parent = None, atts = None):
        T_HandlerBase.__init__(self, parser, parent, atts)

    def child(self, name, atts):
        if name[:len(trex_ns)+1] == trex_ns+"^":
            self.using_trex_ns = 1
        else:
            self.using_trex_ns = 0
        if not handlePattern(self.parser, self, name, atts):
            raise TREXError, "%s not supported as root" % name

    def add_pattern(self, pattern):
        self.product = pattern


def in_trex_ns(name):
    return name[:len(trex_ns)+1] == trex_ns+"^"


def in_default_ns(name):
    return not "^" in name


def trex_ncname(name, using_trex_ns):
    if in_trex_ns(name):
        if using_trex_ns:
            return name[len(trex_ns)+1:]
        else:
            raise TREXError, "root pattern isn't in trex namespace but descendant is"
    else:
        if using_trex_ns:
            return ""
        else:
            return name


def handleNameClass(parser, handler, name, atts):
    name = trex_ncname(name, handler.using_trex_ns)
    if name == "name":
        T_NameHandler(parser, handler, atts)
    elif name == "anyName":
        T_AnyNameHandler(parser, handler, atts)
    elif name == "nsName":
        T_NSNameHandler(parser, handler, atts)
    elif name == "choice":
        T_NameClass_ChoiceHandler(parser, handler, atts)
    elif name == "difference":
        T_DifferenceHandler(parser, handler, atts)
    elif name == "not":
        T_NotHandler(parser, handler, atts)
    else:
        return 0
    return 1


def handlePattern(parser, handler, name, atts):
    name = trex_ncname(name, handler.using_trex_ns)
    if name=="element":
        T_ElementHandler(parser, handler, atts)
    elif name=="empty":
        T_EmptyHandler(parser, handler, atts)
    elif name=="notAllowed":
        T_NotAllowedHandler(parser, handler, atts)
    elif name=="zeroOrMore":
        T_ZeroOrMoreHandler(parser, handler, atts)
    elif name=="oneOrMore":
        T_OneOrMoreHandler(parser, handler, atts)
    elif name=="anyString":
        T_AnyStringHandler(parser, handler, atts)
    elif name=="string":
        T_StringHandler(parser, handler, atts)
    elif name=="optional":
        T_OptionalHandler(parser, handler, atts)
    elif name=="choice":
        T_ChoiceHandler(parser, handler, atts)
    elif name=="concur":
        T_ConcurHandler(parser, handler, atts)
    elif name=="interleave":
        T_InterleaveHandler(parser, handler, atts)
    elif name=="mixed":
        T_MixedHandler(parser, handler, atts)
    elif name=="group":
        T_GroupHandler(parser, handler, atts)
    elif name=="attribute":
        T_AttributeHandler(parser, handler, atts)
    elif name=="grammar":
        T_GrammarHandler(parser, handler, atts)
    elif name=="ref":
        T_RefHandler(parser, handler, atts)
    elif name=="include":
        T_IncludeHandler(parser, handler, atts)
    elif name=="data":
        T_DataHandler(parser, handler, atts)
    else:
        return 0
    return 1


class T_ElementHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.product = T_Element()
        if atts.has_key("name"):
            name = atts["name"]
            if ":" in name:
                # QName
                from string import split
                prefix, ncname = split(name, ":")
                if self.ns_decls.has_key(prefix):
                    ns = self.ns_decls[prefix]
                else:
                    raise TREXError, "QName %s has unknown prefix" % name
            else:
                ns = self.ns_attr
                ncname = name
            self.add_nameclass(ExpandedName(ns, ncname))

    child = T_HandlerBase.child_nameclass_pattern
                    
    def end(self, name):
        if self.product.name_class==None:
            raise TREXError, "element must have a name"
        self.parent.add_pattern(self.product)
        T_HandlerBase.end(self, name)

    def add_nameclass(self, name_class):
        self.product.name_class = name_class

    def add_pattern(self, pattern):
        if self.product.pattern==None:
            self.product.pattern = pattern
        else:
            group = T_Group(self.product.pattern, pattern)
            self.product.pattern = group


class T_AttributeHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.product = T_Attribute()
        if atts.has_key("ns"):
            local_ns = atts["ns"]
        else:
            local_ns = ""
        if atts.has_key("global") and atts["global"] == "true":
            ns = self.ns_attr
        else:
            ns = local_ns
        if atts.has_key("name"):
            name = atts["name"]
            if ":" in name:
                # QName
                from string import split
                prefix, ncname = split(name, ":")
                if self.ns_decls.has_key(prefix):
                    ns = self.ns_decls[prefix]
                else:
                    raise TREXError, "QName %s has unknown prefix" % name
            else:
                # ns already established earlier
                ncname = name
            self.add_nameclass(ExpandedName(ns, ncname))

    child = T_HandlerBase.child_nameclass_pattern

    def end(self, name):
        if self.product.name_class==None:
            raise TREXError, "attribute must have a name"
        if self.product.pattern==None:
            self.product.pattern = T_AnyString()
        self.parent.add_pattern(self.product)
        T_HandlerBase.end(self, name)

    def add_nameclass(self, name_class):
        self.product.name_class = name_class

    def add_pattern(self, pattern):
        self.product.pattern = pattern


class T_NameHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.product = ExpandedName()
        self.chardata = ""

    def char(self, data):
        self.chardata = self.chardata + data

    child = T_HandlerBase.child_none

    def end(self, name):
        self.product.namespaceURI = ""
        self.product.NCName = self.chardata
        self.parent.add_nameclass(self.product)
        T_HandlerBase.end(self, name)


class T_AnyNameHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.product = AnyName()

    def char(self, data):
        raise TREXError, "anyName should not have character data"

    child = T_HandlerBase.child_non_trex

    def end(self, name):
        self.parent.add_nameclass(self.product)
        T_HandlerBase.end(self, name)


class T_NSNameHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.product = NSName(self.ns_attr)

    def char(self, data):
        raise TREXError, "nsName should not have character data"

    child = T_HandlerBase.child_non_trex

    def end(self, name):
        self.parent.add_nameclass(self.product)
        T_HandlerBase.end(self, name)


class T_EmptyHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.product = T_Empty()
        
    def char(self, data):
        raise TREXError, "empty should not have character data"

    child = T_HandlerBase.child_non_trex

    def end(self, name):
        self.parent.add_pattern(self.product)
        T_HandlerBase.end(self, name)


class T_NotAllowedHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.product = T_NotAllowed()
        
    def char(self, data):
        raise TREXError, "notAllowed should not have character data"

    child = T_HandlerBase.child_non_trex

    def end(self, name):
        self.parent.add_pattern(self.product)
        T_HandlerBase.end(self, name)


class T_AnyStringHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.product = T_AnyString()
        
    def char(self, data):
        raise TREXError, "anyString should not have character data"

    child = T_HandlerBase.child_non_trex

    def end(self, name):
        self.parent.add_pattern(self.product)
        T_HandlerBase.end(self, name)


class T_StringHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.chardata = ""
        self.whitespace_normalize = 1
        if atts.has_key("whiteSpace"):
            if atts["whiteSpace"]=="normalize":
                self.whitespace_normalize = 1
            elif atts["whiteSpace"]=="preserve":
                self.whitespace_normalize = 0
            else:
                raise TREXError, "whiteSpace attribute on string must be normalize or preserve, not %s" % atts["whiteSpace"]
        
    def char(self, data):
        self.chardata = self.chardata + data

    child = T_HandlerBase.child_non_trex

    def end(self, name):
        self.parent.add_pattern(T_String(self.chardata, self.whitespace_normalize))
        T_HandlerBase.end(self, name)


class T_DataHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        if atts.has_key("type"):
            type = atts["type"]
            if ":" in type:
                # QName
                from string import split
                prefix, ncname = split(type, ":")
                if self.ns_decls.has_key(prefix):
                    ns = self.ns_decls[prefix]
                else:
                    raise TREXError, "QName %s has unknown prefix" % name
            else:
                ns = self.ns_attr
                ncname = type
            self.type_namespace = ns
            self.type_ncname = ncname
        else:
            raise TREXError, "data must have type attribute"
        
    def char(self, data):
        raise TREXError, "data should not have character data"

    child = T_HandlerBase.child_non_trex

    def end(self, name):
        self.parent.add_pattern(T_Data(self.type_namespace, self.type_ncname))
        T_HandlerBase.end(self, name)


class T_IncludeHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        if atts.has_key("href"):
            self.product = parse_TREX(atts["href"])
        else:
            raise TREXError, "include must have href attribute"
        
    def char(self, data):
        raise TREXError, "include should not have character data"

    child = T_HandlerBase.child_non_trex

    def end(self, name):
        self.parent.add_pattern(self.product)
        T_HandlerBase.end(self, name)
    

class T_ZeroOrMoreHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)

    child = T_HandlerBase.child_pattern

    def end(self, name):
        self.parent.add_pattern(self.product)
        T_HandlerBase.end(self, name)

    def add_pattern(self, pattern):
        self.product = T_Choice(T_Empty(), T_OneOrMore(pattern))


class T_MixedHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)

    child = T_HandlerBase.child_pattern

    def end(self, name):
        self.parent.add_pattern(self.product)
        T_HandlerBase.end(self, name)

    def add_pattern(self, pattern):
        self.product = T_Interleave(T_AnyString(), pattern)


class T_OneOrMoreHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)

    child = T_HandlerBase.child_pattern

    def end(self, name):
        self.parent.add_pattern(self.product)
        T_HandlerBase.end(self, name)

    def add_pattern(self, pattern):
        self.product = T_OneOrMore(pattern)


class T_OptionalHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)

    child = T_HandlerBase.child_pattern

    def end(self, name):
        self.parent.add_pattern(self.product)
        T_HandlerBase.end(self, name)

    def add_pattern(self, pattern):
        self.product = T_Choice(T_Empty(), pattern)


class T_ChoiceHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.pattern_1 = None
        self.pattern_2 = None

    child = T_HandlerBase.child_pattern

    def end(self, name):
        self.parent.add_pattern(self.product)
        T_HandlerBase.end(self, name)

    def add_pattern(self, pattern):
        if self.pattern_1==None:
            self.pattern_1 = pattern
            self.product = self.pattern_1
        elif self.pattern_2==None:
            self.pattern_2 = pattern
            self.product = T_Choice(self.pattern_1, self.pattern_2)
        else:
            self.product = T_Choice(self.product, pattern)


class T_ConcurHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.pattern_1 = None
        self.pattern_2 = None

    child = T_HandlerBase.child_pattern

    def end(self, name):
        self.parent.add_pattern(self.product)
        T_HandlerBase.end(self, name)

    def add_pattern(self, pattern):
        if self.pattern_1==None:
            self.pattern_1 = pattern
            self.product = self.pattern_1
        elif self.pattern_2==None:
            self.pattern_2 = pattern
            self.product = T_Concur(self.pattern_1, self.pattern_2)
        else:
            self.product = T_Concur(self.product, pattern)


class T_NameClass_ChoiceHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.nameclass_1 = None
        self.nameclass_2 = None

    child = T_HandlerBase.child_nameclass

    def end(self, name):
        self.parent.add_nameclass(self.product)
        T_HandlerBase.end(self, name)

    def add_nameclass(self, nameclass):
        if self.nameclass_1==None:
            self.nameclass_1 = nameclass
            self.product = self.nameclass_1
        elif self.nameclass_2==None:
            self.nameclass_2 = nameclass
            self.product = NameClassChoice(self.nameclass_1, self.nameclass_2)
        else:
            self.product = NameClassChoice(self.product, nameclass)


class T_NotHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.nameclass = None

    child = T_HandlerBase.child_nameclass

    def end(self, name):
        self.parent.add_nameclass(self.product)
        T_HandlerBase.end(self, name)

    def add_nameclass(self, nameclass):
        self.product = Difference(AnyName(), nameclass)
    

class T_DifferenceHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.nameclass_1 = None
        self.nameclass_2 = None

    child = T_HandlerBase.child_nameclass

    def end(self, name):
        self.parent.add_nameclass(self.product)
        T_HandlerBase.end(self, name)

    def add_nameclass(self, nameclass):
        if self.nameclass_1==None:
            self.nameclass_1 = nameclass
            self.product = self.nameclass_1
        elif self.nameclass_2==None:
            self.nameclass_2 = nameclass
            self.product = Difference(self.nameclass_1, self.nameclass_2)
        else:
            self.product = Difference(self.product, nameclass)


class T_InterleaveHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.pattern_1 = None
        self.pattern_2 = None

    child = T_HandlerBase.child_pattern

    def end(self, name):
        self.parent.add_pattern(self.product)
        T_HandlerBase.end(self, name)

    def add_pattern(self, pattern):
        if self.pattern_1==None:
            self.pattern_1 = pattern
            self.product = self.pattern_1
        elif self.pattern_2==None:
            self.pattern_2 = pattern
            self.product = T_Interleave(self.pattern_1, self.pattern_2)
        else:
            self.product = T_Interleave(self.product, pattern)


class T_GroupHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.pattern_1 = None

    child = T_HandlerBase.child_pattern

    def end(self, name):
        self.parent.add_pattern(self.product)
        T_HandlerBase.end(self, name)

    def add_pattern(self, pattern):
        if self.pattern_1==None:
            self.product = self.pattern_1 = pattern
        else:
            self.product = self.pattern_1 = T_Group(self.pattern_1, pattern)


class T_GrammarHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.product = T_Grammar()
            
    def child(self, name, atts):
        ncname = trex_ncname(name, self.using_trex_ns)
        if ncname=="start":
            T_StartHandler(self.parser, self, atts)
        elif ncname=="define":
            T_DefineHandler(self.parser, self, atts)
        elif ncname=="include":
            T_IncludeGrammarHandler(self.parser, self, atts)
        else:
            self.child_non_trex(name, atts)

    def end(self, name):
        if self.product.start==None:
            raise TREXError, "grammar must have a start"
        self.parent.add_pattern(self.product)
        T_HandlerBase.end(self, name)

    def set_start(self, pattern, combine=None):
        if self.product.start==None:
            self.product.start = pattern
        else:
            if combine=="replace":
                self.product.start = pattern
            elif combine=="choice":
                self.product.start = T_Choice(self.product.start, pattern)
            elif combine=="group":
                self.product.start = T_Group(self.product.start, pattern)
            elif combine=="interleave":
                self.product.start = T_Interleave(self.product.start, pattern)
            elif combine=="concur":
                raise TREXError, "combine='%s' not supported yet" % combine
            elif combine==None:
                self.product.start = pattern #TODO is this allowed?
            else:
                raise TREXError, "unknown value %s for combine" % combine
        
    def add_definition(self, name, pattern, combine=None):
        if not self.product.definitions.has_key(name):
            self.product.add_definition(name, pattern)
        else:
            if combine=="replace":
                self.product.add_definition(name, pattern)
            elif combine=="choice":
                self.product.add_definition(name, T_Choice(self.product.definitions[name], pattern))
            elif combine=="group":
                self.product.add_definition(name, T_Group(self.product.definitions[name], pattern))
            elif combine=="interleave":
                self.product.add_definition(name, T_Interleave(self.product.definitions[name], pattern))
            elif combine=="concur":
                raise TREXError, "combine='%s' not supported yet" % combine
            elif combine==None:
                raise TREXError, "overriding '%s' of grammar" % name
            else:
                raise TREXError, "unknown value %s for combine" % combine


class T_IncludeGrammarHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        if atts.has_key("href"):
            self.product = parse_TREX(atts["href"])
        else:
            raise TREXError, "include must have href attribute"
        
    def char(self, data):
        raise TREXError, "include should not have character data"

    child = T_HandlerBase.child_non_trex

    def end(self, name):
        self.parent.set_start(self.product.start)
        for definition_name in self.product.definitions.keys():
            self.parent.add_definition(definition_name, self.product.definitions[definition_name])
        T_HandlerBase.end(self, name)


class T_StartHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.product = None
        if atts.has_key("name"):
            self.name = atts["name"]
        else:
            self.name = None
        if atts.has_key("combine"):
            self.combine = atts["combine"]
        else:
            self.combine = None
    
    child = T_HandlerBase.child_pattern

    def end(self, name):
        if self.product==None:
            raise TREXError, "start must contain a pattern"
        self.parent.set_start(self.product)
        if self.name != None:
            self.parent.add_definition(self.name, self.product, self.combine)
        T_HandlerBase.end(self, name)

    def add_pattern(self, pattern):
        self.product = pattern


class T_RefHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        if atts.has_key("name"):
            name = atts["name"]
        else:
            raise TREXError, "ref must have name attribute"
        if atts.has_key("parent"):
            if atts["parent"] == "true":
                parent = 1
            elif atts["parent"] == "false":
                parent = 0
            else:
                raise TREXError, "ref parent attribute must be 'true' or 'false', not '%s'" % atts["parent"]
        else:
            parent = 0
        self.product = T_Ref(name, parent)
        
    def char(self, data):
        raise TREXError, "ref should not have character data"

    child = T_HandlerBase.child_non_trex

    def end(self, name):
        self.parent.add_pattern(self.product)
        T_HandlerBase.end(self, name)


class T_DefineHandler(T_HandlerBase):
    def __init__(self, parser, parent, atts):
        T_HandlerBase.__init__(self, parser, parent, atts)
        self.pattern = None
        if atts.has_key("name"):
            self.name = atts["name"]
        else:
            raise TREXError, "define must have a name"
        if atts.has_key("combine"):
            self.combine = atts["combine"]
        else:
            self.combine = None

    child = T_HandlerBase.child_pattern

    def end(self, name):
        self.parent.add_definition(self.name, self.pattern, self.combine)
        T_HandlerBase.end(self, name)

    def add_pattern(self, pattern):
        if self.pattern==None:
            self.pattern = pattern
        else:
            self.pattern = T_Group(self.pattern, pattern)



########################################################################
### TREX REPRESENTATION / VALIDATION

def validate(trex, instance):
    return trex.M({}, instance.children, {})


class Pattern:
    # each pattern has the following methods:
    # 
    # display()
    #   prints a string representation of the pattern
    #   (recursing over components)
    #
    # M(a,c,e)
    #   returns a Match object indicating whether the match succeeded or,
    #   if not, why not
    #
    # M_consume(a,c,e)
    #   similar to M above but allows for the match to consume only part of
    #   a and c. Because of non-determinism, multiple consumptions are possible
    #   and so the Match object returned will contain a list of possible
    #   remainders unless no matches are possible
    #
    # M_interleave(a,c,e)
    #   similar to M_consume but implements interleaving by allowing
    #   consumption from any part of the given c
    pass


class Match:
    # returned by M and M_consume
    def __init__(self, remainder=None):
        if remainder==None:
            self.remainders = []
        else:
            self.remainders = [remainder]

    def add(self, match):
        self.remainders.extend(match.remainders)

    def isError(self):
        return 0

    def display(self):
        print "(MATCH [",
        for remainder in self.remainders:
            remainder.display()
        print "] )",

    def __repr__(self):
        return "<match %s>" % self.remainders

    def __cmp__(self, other):
        if self.remainders == other.remainders:
            return 0
        else:
            return -1

class Error(Match):
    def __init__(self, message, *children):
        self.message = message
        self.children = children
        
    def isError(self):
        return 1

    def display(self):
        print "(ERROR",
        print self.message,
        for error in self.children:
            error.display()
        print ")",


class Remainder:
    def __init__(self, a, c):
        self.a = a
        self.c = c

    def display(self):
        print "(",self.a, "[",
        for node in self.c:
            node.display()
        print "] )",

    def __repr__(self):
        return "<%s,%s>" % (self.a, self.c)

    def __cmp__(self, other):
        if other==None:
            return -1
        if self.a != other.a:
            return -1
        if self.c != other.c:
            return -1
        return 0


class Environment:
    def __init__(self, e={}, parent=None):
        self.e = e
        self.parent = parent


def normalize(s):
    ns = ""
    state = 0
    for c in s:
        if state==0:
            if c in [chr(9),chr(10),chr(13),chr(32)]:
                continue
            else:
                ns = ns + c
                state=1
                continue
        elif state==1:
            if c in [chr(9),chr(10),chr(13),chr(32)]:
                state=2
                continue
            else:
                ns = ns + c
                continue
        elif state==2:
            if c in [chr(9),chr(10),chr(13),chr(32)]:
                continue
            else:
                ns = ns + " " + c
                state=1
    return ns


datatype_registry = {}


# test_function must take a string and return a boolean (ie 1 or 0)
def register_datatype(namespace_uri, ncname, test_function):
    datatype_registry[namespace_uri + "^" + ncname] = test_function


def allows(namespace_uri, ncname, s):
    key = namespace_uri + "^" + ncname
    if datatype_registry.has_key(key):
        if datatype_registry[namespace_uri + "^" + ncname](s):
            return Match()
        else:
            return Error("'%s' not allowed by '%s' in '%s'" % (s, ncname, namespace_uri))
    else:
        return Error("unknown datatype '%s' in '%s'" % (ncname, namespace_uri))


# sample datatype test function (used by tests)
def is_integer(cdata):
    try:
        int(cdata)
    except ValueError:
        return 0
    return 1

# sample datatype registration
register_datatype("http://pytrex.sourceforge.net/2001/03", "integer", is_integer)


class T_Element(Pattern):
    def __init__(self, name_class=None, pattern=None):
        self.name_class = name_class
        self.pattern = pattern

    def display(self):
        print "(ELEMENT",
        self.name_class.display()
        self.pattern.display()
        print ")",

    def M(self, a, c, e):
        if len(a) > 0:
            return Error("has attributes")
        c_state=0
        for node in c:
            if node.is_whitespace():
                continue
            if node.is_element():
                if c_state==1:
                    return Error("second element")
                n = node.expanded_name
                a_1 = node.attributes
                c_1 = node.children
                c_state=1
        if c_state==0:
            return Error("no element")
        match = self.name_class.C(n)
        if match.isError():
            return Error("name doesn't match", match)
        match = self.pattern.M(a_1,c_1,e)
        if match.isError():
            return Error("pattern doesn't match", match)
        return Match()

    def M_consume(self, a, c, e):
        c_state=0
        for pos in range(0,len(c)):
            if c[pos].is_whitespace():
                continue
            if c[pos].is_element():
                if c_state==1:
                    return Match(Remainder(a, c[pos:]))
                n = c[pos].expanded_name
                a_1 = c[pos].attributes
                c_1 = c[pos].children
                c_state=1
                match = self.name_class.C(n)
                if match.isError():
                    return Error("name doesn't match", match)
                match = self.pattern.M(a_1, c_1, e)
                if match.isError():
                    return Error("pattern doesn't match", match)
        if c_state==0:
            return Error("no element")
        match = self.name_class.C(n)
        if match.isError():
            return Error("name doesn't match", match)
        match = self.pattern.M(a_1, c_1, e)
        if match.isError():
            return Error("pattern doesn't match", match)
        return Match(Remainder(a, []))

    def M_interleave(self, a, c, e):
        c_2 = []
        taken = 0
        for pos in range(0,len(c)):
            if c[pos].is_element():
                n = c[pos].expanded_name
                a_1 = c[pos].attributes
                c_1 = c[pos].children
                match = self.name_class.C(n)
                if match.isError():
                    c_2.append(c[pos])
                    continue
                match = self.pattern.M(a_1, c_1, e)
                if match.isError():
                    c_2.append(c[pos])
                    continue
                taken = 1
            else:
                c_2.append(c[pos])
        if taken:
            return Match(Remainder(a, c_2))
        else:
            return Error("element in interleave did not match")


class T_Attribute(Pattern):
    def __init__(self, name_class=None, pattern=None):
        self.name_class = name_class
        self.pattern = pattern

    def display(self):
        print "(ATTRIBUTE",
        self.name_class.display()
        self.pattern.display()
        print ")",

    def M(self, a, c, e):
        if len(c)>0:
            return Error("has children when should be empty")
        if len(a)!=1:
            return Error("incorrect number of attributes")
        n = a[0].expanded_name
        v = a[0].value
        match_1 = self.name_class.C(n)
        match_2 = self.pattern.M({}, v, e)
        if (not match_1.isError()) and (not match_2.isError()):
            return Match()
        return Error("attribute did not match")

    def M_consume(self, a, c, e):
        for attr in a:
            n = attr.expanded_name
            v = attr.value
            match_1 = self.name_class.C(n)
            match_2 = self.pattern.M({}, v, e)
            if (not match_1.isError()) and (not match_2.isError()):
                a_2 = []
                for attr2 in a:
                    if attr2 != attr:
                        a_2.append(attr2)
                return Match(Remainder(a_2,c))
        return Error("attribute didn't match") # or should this be Match(Remainder(a,c))

    M_interleave = M_consume


class T_Empty(Pattern):
    def display(self):
        print "(EMPTY)",
        
    def M(self, a, c, e):
        if len(a) > 0:
            return Error("has attributes")
        if len(c) > 0:
            return Error("has children when should be empty")
        return Match()

    def M_consume(self, a, c, e):
        return Match(Remainder(a,c))

    M_interleave = M_consume


class T_NotAllowed(Pattern):
    def display(self):
        print "(NOT-ALLOWED)",
        
    def M(self, a, c, e):
        return Error("not allowed")

    M_consume = M
    M_interleave = M


class T_AnyString(Pattern):
    def display(self):
        print "(ANY-STRING)",
        
    def M(self, a, c, e):
        if len(a) > 0:
            return Error("has attributes")
        for node in c:
            if node.is_element():
                return Error("anyString but got element")
        return Match()

    def M_consume(self, a, c, e):
        if len(a) > 0:
            return Error("has attributes")
        if len(c)==0:
            return Error("anyString but no children")
        for pos in range(0,len(c)):
            if c[pos].is_element():
                if pos==0:
                    return Error("element where string required")
                else:
                    return Match(Remainder(a,c[pos:]))
        return Match(Remainder(a,[]))

    def M_interleave(self, a, c, e):
        c_2 = []
        taken = 0
        for pos in range(0, len(c)):
            if c[pos].is_element():
                c_2.append(c[pos])
            else:
                taken=1
        if taken:
            return Match(Remainder(a, c_2))
        else:
            return Error("anyString but no characters") # TODO maybe this is okay!?!?


class T_String(Pattern):
    def __init__(self, chardata, whitespace_normalize):
        self.chardata = chardata
        self.whitespace_normalize = whitespace_normalize
        
    def display(self):
        print "(STRING '%s')" % self.chardata

    def M(self, a, c, e):
        if len(a) > 0:
            return Error("has attributes")
        cdata = ""
        for node in c:
            if node.is_element():
                return Error("string but got element")
            else:
                 cdata = cdata + node.data
        if self.whitespace_normalize:
            if normalize(cdata) == normalize(self.chardata):
                return Match()
            else:
                return Error("character data '%s' did not match string '%s'" % (normalize(cdata), normalize(self.chardata)))
        else:
            if cdata == self.chardata:
                return Match()
            else:
                return Error("character data '%s' did not match string '%s'" % (cdata, self.chardata))

    # TODO should flag an error in the following cases as string shouldn't
    # appear in group or interleave
    M_consume = M
    M_interleave = M


class T_Data(Pattern):
    def __init__(self, type_namespace, type_ncname):
        self.type_namespace = type_namespace
        self.type_ncname = type_ncname
        
    def display(self):
        print "(DATA '%s' '%s')" % (self.type_namespace, self.type_ncname)

    def M(self, a, c, e):
        if len(a) > 0:
            return Error("has attributes")
        cdata = ""
        for node in c:
            if node.is_element():
                return Error("string but got element")
            else:
                 cdata = cdata + node.data
        return allows(self.type_namespace, self.type_ncname, cdata)

    # TODO should flag an error in the following cases as data shouldn't
    # appear in group or interleave
    M_consume = M
    M_interleave = M


class T_Choice(Pattern):
    def __init__(self, pattern_1=None, pattern_2=None):
        self.pattern_1 = pattern_1
        self.pattern_2 = pattern_2

    def display(self):
        print "(CHOICE",
        self.pattern_1.display()
        self.pattern_2.display()
        print ")",
        
    def M(self, a, c, e):
        match_1 = self.pattern_1.M(a, c ,e)
        if not match_1.isError():
            return Match()
        match_2 = self.pattern_2.M(a, c, e)
        if not match_2.isError():
            return Match()
        return Error("both items of a choice failed", match_1, match_2)

    def M_consume(self, a, c, e):
        match = Match()
        match_1 = self.pattern_1.M_consume(a, c ,e)
        if not match_1.isError():
            match.add(match_1)
        match_2 = self.pattern_2.M_consume(a, c, e)
        if not match_2.isError():
            match.add(match_2)
        if match_1.isError() and match_2.isError():
            return Error("both items of a choice failed", match_1, match_2)
        return match

    def M_interleave(self, a, c, e):
        match = Match()
        match_1 = self.pattern_1.M_interleave(a, c ,e)
        if not match_1.isError():
            match.add(match_1)
        match_2 = self.pattern_2.M_interleave(a, c, e)
        if not match_2.isError():
            match.add(match_2)
        if match_1.isError() and match_2.isError():
            return Error("both items of a choice failed", match_1, match_2)
        return match


class T_Concur(Pattern):
    def __init__(self, pattern_1=None, pattern_2=None):
        self.pattern_1 = pattern_1
        self.pattern_2 = pattern_2

    def display(self):
        print "(CONCUR",
        self.pattern_1.display()
        self.pattern_2.display()
        print ")",
        
    def M(self, a, c, e):
        match_1 = self.pattern_1.M(a, c ,e)
        if match_1.isError():
            return match_1
        match_2 = self.pattern_2.M(a, c, e)
        if match_2.isError():
            return match_2
        return Match()

    def M_consume(self, a, c, e):
        match_1 = self.pattern_1.M_consume(a, c ,e)
        if match_1.isError():
            return match_1
        match_2 = self.pattern_2.M_consume(a, c, e)
        if match_2.isError():
            return match_2
        if match_1 == match_2:
            return match_1
        else:
            return Error("two patterns of concur consumed different amounts")

    def M_interleave(self, a, c, e):
        match_1 = self.pattern_1.M_interleave(a, c ,e)
        if match_1.isError():
            return match_1
        match_2 = self.pattern_2.M_interleave(a, c, e)
        if match_2.isError():
            return match_2
        if match_1 == match_2:
            return match_1
        else:
            return Error("two patterns of concur interleaved different amounts")


class T_Interleave(Pattern):
    def __init__(self, pattern_1=None, pattern_2=None):
        self.pattern_1 = pattern_1
        self.pattern_2 = pattern_2

    def display(self):
        print "(INTERLEAVE",
        self.pattern_1.display()
        self.pattern_2.display()
        print ")",

    def M(self, a, c, e):
        match_1 = self.pattern_1.M_interleave(a,c,e)
        if match_1.isError():
            return Error("first pattern of interleave failed", match_1)
        match = Match()
	for remainder in match_1.remainders:
	    a_2 = remainder.a
            c_2 = remainder.c
            match = self.pattern_2.M(a_2, c_2, e)
            if not match.isError():
                return Match()
        return Error("second pattern of interleave failed", match)

    def M_consume(self, a, c, e):
        match_1 = self.pattern_1.M_interleave(a,c,e)
        if match_1.isError():
            return Error("first pattern of interleave failed", match_1)
        match = Match()
	for remainder in match_1.remainders:
	    a_2 = remainder.a
            c_2 = remainder.c
            match = self.pattern_2.M_consume(a_2, c_2, e)
            if not match.isError():
                return match
        return Error("second pattern of interleave failed", match)

    def M_interleave(self, a, c, e):
        match_1 = self.pattern_1.M_interleave(a,c,e)
        if match_1.isError():
            return Error("first pattern of interleave failed", match_1)
        match = Match()
	for remainder in match_1.remainders:
	    a_2 = remainder.a
            c_2 = remainder.c
            match_2 = self.pattern_2.M_interleave(a_2, c_2, e)
            if not match.isError():
                match.add(match_2)
        return match
        

class T_OneOrMore(Pattern):
    def __init__(self, pattern=None):
        self.pattern = pattern

    def display(self):
        print "(ONE-OR-MORE",
        self.pattern.display()
        print ")",

    def M(self, a, c, e):
        group = T_Group(self.pattern, T_Choice(T_Empty(), T_OneOrMore(self.pattern)))
        match = group.M(a, c, e)
        if match.isError():
            return Error("oneOrMore failed")
        return Match()

    def M_consume(self, a, c, e):
        group = T_Group(self.pattern, T_Choice(T_Empty(), T_OneOrMore(self.pattern)))
        return group.M_consume(a, c, e)

    def M_interleave(self, a, c, e):
        group = T_Group(self.pattern, T_Choice(T_Empty(), T_OneOrMore(self.pattern)))
        return group.M_interleave(a, c, e)
   

class T_Group(Pattern):
    def __init__(self, pattern_1=None, pattern_2=None):
        self.pattern_1 = pattern_1
        self.pattern_2 = pattern_2

    def display(self):
        print "(GROUP",
        self.pattern_1.display()
        self.pattern_2.display()
        print ")",

    def M(self, a, c, e):
        match_1 = self.pattern_1.M_consume(a,c,e)
        if match_1.isError():
            return Error("first pattern of group failed", match_1)
        match = Match()
	for remainder in match_1.remainders:
	    a_2 = remainder.a
            c_2 = remainder.c
            match = self.pattern_2.M(a_2, c_2, e)
            if not match.isError():
                return Match()
        return Error("second pattern of group failed", match)

    def M_consume(self, a, c, e):
        match_1 = self.pattern_1.M_consume(a,c,e)
        if match_1.isError():
            return Error("first pattern of group failed", match_1)
        match = Match()
        for remainder in match_1.remainders:
            a_2 = remainder.a
            c_2 = remainder.c
            match_2 = self.pattern_2.M_consume(a_2, c_2, e)
            if not match_2.isError():
                match.add(match_2)
        return match

    def M_interleave(self, a, c, e):
        # TODO I'm not 100% what it means to interleave a group (eg does order matter?)
        match_1 = self.pattern_1.M_interleave(a,c,e)
        if match_1.isError():
            return Error("first pattern of group failed", match_1)
        match = Match()
        for remainder in match_1.remainders:
            a_2 = remainder.a
            c_2 = remainder.c
            match_2 = self.pattern_2.M_interleave(a_2, c_2, e)
            if not match_2.isError():
                match.add(match_2)
        return match


class T_Grammar(Pattern):
    def __init__(self):
        self.start = None
        self.definitions = {}

    def display(self):
        print "(GRAMMAR",
        self.start.display()
        for definition in self.definitions.keys():
            print "(%s=" % definition,
            self.definitions[definition].display()
            print ")",
        print ")",

    def add_definition(self, name, definition):
        self.definitions[name] = definition

    def M(self, a, c, e):
        return self.start.M(a, c, Environment(self.definitions, e))

    def M_consume(self, a, c, e):
        return self.start.M_consume(a, c, Environment(self.definitions, e))

    def M_interleave(self, a, c, e):
        return self.start.M_interleave(a, c, Environment(self.defintions, e))


class T_Ref(Pattern):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        
    def display(self):
        print "(REF =%s %s)" % (self.name, self.parent)

    def M(self, a, c, e):
        if self.parent == 0:
            if not e.e.has_key(self.name):
                return Error("ref to unknown pattern '%s'" % self.name)
            else:
                pattern = e.e[self.name]
                return pattern.M(a, c, e)
        else:
            if not e.parent.e.has_key(self.name):
                return Error("ref to unknown pattern '%s'" % self.name)
            else:
                pattern = e.parent.e[self.name]
                return pattern.M(a, c, e.parent)
            

    def M_consume(self, a, c, e):
        if self.parent == 0:
            if not e.e.has_key(self.name):
                return Error("ref to unknown pattern '%s'" % self.name)
            else:
                pattern = e.e[self.name]
                return pattern.M_consume(a, c, e)
        else:
            if not e.parent.e.has_key(self.name):
                return Error("ref to unknown pattern '%s'" % self.name)
            else:
                pattern = e.parent.e[self.name]
                return pattern.M_consume(a, c, e.parent)

    def M_interleave(self, a, c, e):
        if self.parent == 0:
            if not e.e.has_key(self.name):
                return Error("ref to unknown pattern '%s'" % self.name)
            else:
                pattern = e.e[self.name]
                return pattern.M_interleave(a, c, e)
        else:
            if not e.parent.e.has_key(self.name):
                return Error("ref to unknown pattern '%s'" % self.name)
            else:
                pattern = e.parent.e[self.name]
                return pattern.M_interleave(a, c, e.parent)


class NameClass:
    pass


class ExpandedName(NameClass):
    def __init__(self, namespaceURI=None, NCName=None):
        self.namespaceURI = namespaceURI
        self.NCName = NCName

    def display(self):
        print "(EXPANDED-NAME '%s' '%s')" % (self.namespaceURI, self.NCName),

    def C(self, n):
        if self.namespaceURI==n.namespaceURI and self.NCName==n.localName:
            return Match()
        else:
            return Error("expanded name doesn't match: %s^%s != %s^%s" % (self.namespaceURI, self.NCName, n.namespaceURI, n.localName))


class AnyName(NameClass):
    def display(self):
        print "(ANY-NAME)",

    def C(self, n):
        return Match()


class NSName(NameClass):
    def __init__(self, namespaceURI):
        self.namespaceURI = namespaceURI

    def display(self):
        print "(NS-NAME '%s')" % self.namespaceURI

    def C(self, n):
        if self.namespaceURI==n.namespaceURI:
            return Match()
        else:
            return Error("namespace doesn't match: %s != %s" % (self.namespaceURI, n.namespaceURI))


class NameClassChoice(NameClass):
    def __init__(self, nameclass_1, nameclass_2):
        self.nameclass_1 = nameclass_1
        self.nameclass_2 = nameclass_2

    def display(self):
        print "(CHOICE",
        self.nameclass_1.display()
        self.nameclass_2.display()
        print ")",

    def C(self, n):
        match_1 = self.nameclass_1.C(n)
        if not match_1.isError():
            return Match()
        match_2 = self.nameclass_2.C(n)
        if not match_2.isError():
            return Match()
        return Error("both items of a choice failed", match_1, match_2)


class Difference(NameClass):
    def __init__(self, nameclass_1, nameclass_2):
        self.nameclass_1 = nameclass_1
        self.nameclass_2 = nameclass_2

    def display(self):
        print "(DIFFERENCE",
        self.nameclass_1.display()
        self.nameclass_2.display()
        print ")",

    def C(self, n):
        match = self.nameclass_1.C(n)
        if match.isError():
            return Error("first name-class of a difference failed", match)
        match = self.nameclass_2.C(n)
        if not match.isError():
            return Error("second name-class of a difference failed", match)
        return Match()



########################################################################
### INSTANCE REPRESENTATION
#
# Basically the instance data model from section 2
#

class I_Node:
    pass


class I_Root(I_Node):
    def __init__(self):
        self.children = []

    def add_child(self, node):
        self.children.append(node)
        
    def is_whitespace(self):
        return 0

    def is_element(self):
        return 0

    def display(self):
        print "(ROOT",
        for child in self.children:
            child.display()
        print ")"


class I_ExpandedName:
    def __init__(self, namespaceURI, localName):
        self.namespaceURI = namespaceURI
        self.localName = localName


class I_Element(I_Node):
    def __init__(self):
        self.expanded_name = None
        self.attributes = []
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def add_attribute(self, node):
        self.attributes.append(node)

    def is_whitespace(self):
        return 0

    def is_element(self):
        return 1

    def display(self):
        print "(%s" % self.expanded_name.localName,
        for attr in self.attributes:
            attr.display()
        for child in self.children:
            child.display()
        print ")",

    def __repr__(self):
        return "<%s>" % self.expanded_name.localName


class I_Attribute(I_Node):
    def __init__(self, expanded_name=None, value=None):
        self.expanded_name = expanded_name
        self.value = value

    def is_whitespace(self):
        return 0

    def is_element(self):
        return 1

    def display(self):
        print "(@%s" % self.expanded_name.localName,
        self.value[0].display()
        print ")",

    def __repr__(self):
        return "<%s=%s>" % (self.expanded_name.localName, self.value)


class I_CharData(I_Node):
    def __init__(self, data):
        self.data = data
        
    def is_whitespace(self):
        for char in self.data:
            if char not in [chr(9),chr(10),chr(13),chr(32)]:
                return 0
        return 1

    def is_element(self):
        return 0

    def display(self):
        print "'%s'" % self.data,

    def __repr__(self):
        return "'%s'" % self.data
    

########################################################################
### INSTANCE PARSING

# TODO wellformedness errors don't seem to get reported

def parse_Instance(location, baseURI=None):
    if baseURI==None:
        baseURI = location

    import xml.parsers.expat
    parser = xml.parsers.expat.ParserCreate(namespace_separator="^")
    parser.SetBase(baseURI)
    parser.returns_unicode = 1

    i = I_RootHandler(parser)

    from urllib2 import urlopen
    f = urlopen(location)
    try:
        parser.ParseFile(f)
    except xml.parsers.expat.error:
        import sys
        sys.stderr.write("Error parsing file at line '%s' and column '%s'\n" % (parser.ErrorLineNumber, parser.ErrorColumnNumber) )
        sys.stderr.flush()
    f.close()

    return i.product


class I_RootHandler(HandlerBase):
    def __init__(self, parser, parent = None, atts = None):
        HandlerBase.__init__(self, parser, parent, atts)
        self.product = I_Root()

    def child(self, name, atts):
        I_ElementHandler(self.parser, self, name, atts)

    def char(self, data):
        self.product.add_child(I_CharData(data))

    def end(self, name):
        HandlerBase.end(self, name)

    def add_child(self, node):
        self.product.add_child(node)


class I_ElementHandler(HandlerBase):
    def __init__(self, parser, parent, name, atts):
        HandlerBase.__init__(self, parser, parent, atts)
        self.product = I_Element()
        import string
        n = string.split(name,"^")
        if len(n)==1:
            namespaceURI=""
            localName=n[0]
        else:
            namespaceURI=n[0]
            localName=n[1]
        self.product.expanded_name = I_ExpandedName(namespaceURI, localName)
        for attr in atts.keys():
            n = string.split(attr,"^")
            if len(n)==1:
                namespaceURI=""
                localName=n[0]
            else:
                namespaceURI=n[0]
                localName=n[1]
            self.product.add_attribute(I_Attribute(I_ExpandedName(namespaceURI, localName), [I_CharData(atts[attr])]))

    def child(self, name, atts):
        I_ElementHandler(self.parser, self, name, atts)

    def char(self, data):
        self.product.add_child(I_CharData(data))

    def end(self, name):
        self.parent.add_child(self.product)
        HandlerBase.end(self, name)

    def add_child(self, node):
        self.product.add_child(node)



########################################################################
### MAIN LINE

if __name__ == "__main__":
    import sys
    if len(sys.argv)==3:
        match = validate(parse_TREX(sys.argv[1]),parse_Instance(sys.argv[2]))
        if match.isError():
            match.display()
        else:
            print "match"
    else:
        print "usage: python pytrex.py <trex-file> <instance-file>"
