#!/usr/bin/python

"""
This script converts DTDs to XML Schemas, according to the 20000407 WD.
It can do simple reverse-engineering of attribute groups.
"""

# Todo
# - make better names for attrgroups?
# - make a SchemaWriter class (to hold common references)
# - start doing reverse engineering to create modelGroups?

from xml.parsers.xmlproc import xmldtd
import sys, types, os.path, string

usage = \
"""
Usage:

  python dtd2schema.py <inputfile> [<outputfile>]

  Input file names can be URLs.

  If the output file name is omitted, it will be inferred from the
  input file name. Note that this inference does not work for URLs.
"""

version = "0.2"

# ===== UTILITY FUNCTIONS

class CountingDict:

    def __init__(self):
        self._items = {}

    def count(self, item):
        try:
            self._items[item] = self._items[item] + 1
        except KeyError:
            self._items[item] = 1

    def clear(self):
        self._items = {}

    def keys(self):
        return self._items.keys()

    def __getitem__(self, item):
        return self._items[item]

    def __delitem__(self, item):
        del self._items[item]

class AttributeInfo:
    """This class holds information about reverse-engineered attribute
    groupings."""

    def __init__(self):
        self._shared_attrs = {}
        self._shared_attrs_on_elem = {}
        self._count = CountingDict()
        self._groupnames = {}

    def count(self, attrname):
        self._count.count(attrname)

    def new_attr(self, elemname, attr):
        attrname = attr.get_name()
        self._count.count(attrname)

        if self._shared_attrs.has_key(attrname):
            shared = self._shared_attrs[attrname]
            if shared != None and not compare_attrs(shared, attr):
                self._shared_attrs[attrname] = None

        else:
            self._shared_attrs[attrname] = attr

    def remove_single_attributes(self):
        "Removes attributes that only occurred once."
        for attrname in self._shared_attrs.keys():
            if self._shared_attrs.get(attrname) != None:
                if self._count[attrname] < 2:
                    self._shared_attrs[attrname] = None

        self._count.clear()

    def find_groups(self, elem):
        shared = tuple(filter(self._shared_attrs.get, elem.get_attr_list()))
        self._shared_attrs_on_elem[elem.get_name()] = shared
        if shared:
            self._count.count(shared)

    def remove_single_groups(self):
        "Removes groups that only occurred once."
        for group in self._count.keys():
            if self._count[group] < 2:
                del self._count[group]

    def get_groups(self):
        return self._count.keys()

    def get_attribute(self, name):
        return self._shared_attrs[name]

    def get_shared_attrs_on_elem(self, elemname):
        return self._shared_attrs_on_elem[elemname]

    def make_name(self, group):
        name = "group" + str(len(self._groupnames) + 1)
        self._groupnames[group] = name
        return name

    def get_group_name(self, group):
        return self._groupnames[group]

def escape_attr_value(value):
    value = string.replace(value, '&', '&amp;')
    value = string.replace(value, '"', '&quot;')
    return string.replace(value, '<', '&lt;')

# ===== REVERSE ENGINEERING

def compare_attrs(attr1, attr2):
    return attr1.get_name() == attr2.get_name() and \
           attr1.get_type() == attr2.get_type() and \
           attr1.get_decl() == attr2.get_decl() and \
           attr1.get_default() == attr2.get_default()

def find_attr_groups(dtd):
    # first pass: find attributes that occur more than once
    attrinfo = AttributeInfo()
    for elemname in dtd.get_elements():
        elem = dtd.get_elem(elemname)

        for attrname in elem.get_attr_list():
            attrinfo.new_attr(elemname, elem.get_attr(attrname))

    attrinfo.remove_single_attributes()

    # second pass: group the recurring attributes
    for elemname in dtd.get_elements():
        elem = dtd.get_elem(elemname)
        attrinfo.find_groups(elem)

    attrinfo.remove_single_groups()
    return attrinfo

# ===== COMPONENT FUNCTIONS

def write_attribute_group(out, group, attrinfo):
    groupname = attrinfo.make_name(group)
    out.write('  <attributeGroup name="%s">\n' % groupname)
    for attrname in group:
        write_attr(out, attrinfo.get_attribute(attrname))
    out.write('  </attributeGroup>\n')

declmap = {"#REQUIRED" : "required",
           "#IMPLIED"  : "optional",
           "#DEFAULT"  : "default",
           "#FIXED"    : "fixed" }

def write_attr(out, attr):
    value = attr.get_default()
    if value == None:
        value = ''
    else:
        value = ' value="%s"' % escape_attr_value(value)

    attrtype = attr.get_type()
    if type(attrtype) == types.ListType:
        out.write('      <attribute name="%s" use="%s"%s>\n' %
                  (attr.get_name(), declmap[attr.get_decl()], value))
        out.write('        <simpleType base="NMTOKEN">\n')
        for token in attrtype:
            out.write('          <enumeration value="%s"/>\n' % token)
        out.write('        </simpleType>\n')
        out.write('      </attribute>\n')
    else:
        out.write('      <attribute name="%s" type="%s" use="%s"%s/>\n' %
                  (attr.get_name(), attrtype, declmap[attr.get_decl()],
                   value))

def write_attributes(out, elem, attrinfo):
    attrnames = elem.get_attr_list()
    shared = attrinfo.get_shared_attrs_on_elem(elem.get_name()) or []
    for attrname in attrnames:
        if not attrname in shared:
            write_attr(out, elem.get_attr(attrname))

    if shared:
        out.write('      <attributeGroup ref="%s">\n' %
                  attrinfo.get_group_name(group))

def write_element_type(out, elem, attrinfo):
    cm = elem.get_content_model()
    if cm == ('', [('#PCDATA', '')], ''):
        if elem.get_attr_list() == []:
            out.write('    <simpleType ref="string"/>\n')
        else:
            out.write('    <complexType base="string" derivedBy="extension">\n')
            write_attributes(out, elem, attrinfo)
            out.write('    </complexType>\n')
        return

    content = ''
    if cm == ("", [], ""):
        content = ' content="empty"'
    elif cm != None and cm[1][0][0] == "#PCDATA":
        content = ' content="mixed"'

    out.write('    <complexType%s>\n' % content)
    if cm == None:
        out.write('    <any/>\n')
    elif cm != ("", [], ""):
        write_cm(out, cm)

    write_attributes(out, elem, attrinfo)
    out.write('    </complexType>\n')

def write_cm(out, cm):
    (sep, cps, mod) = cm
    out.write('    <group>\n')

    if sep == '' or sep == ',':
        wrapper = 'sequence'
    elif sep == '|':
        wrapper = 'choice'

    out.write('      <%s>\n' % wrapper)
    for cp in cps:
        if len(cp) == 2:
            (name, mod) = cp
            if name == "#PCDATA":
                continue

            if mod == '?':
                occurs = ' minOccurs="0" maxOccurs="1"'
            elif mod == '*':
                occurs = ' minOccurs="0" maxOccurs="*"'
            elif mod == '+':
                occurs = ' minOccurs="1" maxOccurs="*"'
            else:
                occurs = ''

            out.write('        <element ref="%s"%s/>\n' % (name, occurs))
        elif len(cp) == 3:
            write_cm(out, cp)
        else:
            out.write('        <!-- %s -->\n' % (cp,))

    out.write('      </%s>\n' % wrapper)

    out.write('    </group>\n')

# ===== MAIN PROGRAM

# --- Interpreting command-line

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print usage
    sys.exit(1)

infile = sys.argv[1]
if len(sys.argv) == 3:
    outfile = sys.argv[2]
else:
    ext = os.path.splitext(infile)[1]
    outfile = os.path.split(infile)[1]
    outfile = outfile[ : -len(ext)] + ".xsd"

# --- Doing the job

print "\ndtd2schema.py\n"

# Load DTD

print "Loading DTD..."
dtd = xmldtd.load_dtd(infile)

# Find attribute groups

print "Doing reverse-engineering..."
attrinfo = find_attr_groups(dtd)

# Write out schema

print "Writing out schema"
out = open(outfile, "w")

out.write('<?xml version="1.0"?>\n')
out.write('<!--\n')
out.write('  Converted from a DTD by dtd2schema.py, using xmlproc.\n')
out.write('  NOTE: This version is not reliable. It has not been\n')
out.write('  properly checked against the standard (20000407 WD) yet.\n')
out.write('-->\n\n')
out.write('<schema xmlns="http://www.w3.org/1999/XMLSchema">\n\n')

if attrinfo:
    out.write('<!-- ========= ATTRIBUTE GROUP DECLARATIONS ========= -->\n\n')

    for group in attrinfo.get_groups():
        write_attribute_group(out, group, attrinfo)

    out.write("\n")

out.write('<!-- ========== ELEMENT DECLARATIONS ========== -->\n\n')

for elemname in dtd.get_elements():
    elem = dtd.get_elem(elemname)
    out.write('  <element name="%s">\n' % elemname)
    write_element_type(out, elem, attrinfo)
    out.write('  </element>\n\n')

notations = dtd.get_notations()
if notations != []:
    out.write('\n\n<!-- ========== NOTATION DECLARATIONS ========== -->\n\n')

    for notname in notations:
        (pubid, sysid) = dtd.get_notation(notname)
        if sysid == None:
            sysid = ''
        else:
            sysid = ' system="%s"'

        out.write('  <notation name="%s" public="%s"%s>\n' %
                  (notname, pubid, sysid))

out.write('</schema>\n')
out.close()
