#! /usr/bin/env python

# Setup script for the XML tools
#
# Targets: build install help

import sys, os, string

from distutils.core import setup, Extension
from setupext import Data_Files, install_Data_Files, wininst_request_delete
from distutils.sysconfig import get_config_var, get_config_vars
from distutils.sysconfig import parse_config_h, get_config_h_filename

# I want to override the default build directory so the extension
# modules are compiled and placed in the build/xml directory
# tree.  This is a bit clumsy, but I don't see a better way to do
# this at the moment.

ext_modules = []

# Rename xml to _xmlplus for Python 2.x

if sys.hexversion < 0x2000000:
    def xml(s):
        return "xml"+s
else:
    def xml(s):
        return "_xmlplus"+s

# special command-line arguments
LIBEXPAT = None
LDFLAGS = []

args = sys.argv[:]
extra_packages = []
with_xpath = 1
with_xslt = 0

for arg in args:
    if string.find(arg, '--with-libexpat=') == 0:
        LIBEXPAT = string.split(arg, '=')[1]
        sys.argv.remove(arg)
    elif string.find(arg, '--ldflags=') == 0:
        LDFLAGS = string.split(string.split(arg, '=')[1])
        sys.argv.remove(arg)
    elif arg == '--with-xpath':
        with_xpath = 1
        sys.argv.remove(arg)
    elif arg == '--with-xslt':
        with_xslt = 1
	sys.argv.remove(arg)
    elif arg == '--without-xpath':
        with_xpath = 0
        sys.argv.remove(arg)
    elif arg == '--without-xslt':
        with_xslt = 0
	sys.argv.remove(arg)

if sys.platform.startswith("darwin"):
    # Fixup various Mac OS X issues
    if get_config_var("LDSHARED").find("-flat_namespace") == -1:
        LDFLAGS.append('-flat_namespace')
    if get_config_var("LDFLAGS").find("-arch i386") != -1:
        # Remove the erroneous duplicate -arch flag globally
        new_flags = get_config_var('LDFLAGS').replace('-arch i386', '')
        get_config_vars()['LDFLAGS'] = new_flags

if with_xpath:
    extra_packages.append(xml('.xpath'))

if with_xslt:
    extra_packages.append(xml('.xslt'))

def get_expat_prefix():
    if LIBEXPAT:
        return LIBEXPAT

    # XXX temporarily disable usage of installed expat
    # until we figure out a way to determine its version
    return

    for p in ("/usr", "/usr/local"):
        incs = os.path.join(p, "include")
        libs = os.path.join(p, "lib")
        if os.path.isfile(os.path.join(incs, "expat.h")) \
           and (os.path.isfile(os.path.join(libs, "libexpat.so"))
                or os.path.isfile(os.path.join(libs, "libexpat.a"))):
            return p


expat_prefix = get_expat_prefix()

sources = ['extensions/pyexpat.c']
if expat_prefix:
    define_macros = [('HAVE_EXPAT_H', None)]
    include_dirs = [os.path.join(expat_prefix, "include")]
    libraries = ['expat']
    library_dirs = [os.path.join(expat_prefix, "lib")]
else:
    # To build expat 1.95.x, we need to find out the byteorder
    if sys.byteorder == "little":
        xmlbo = "1234"
    else:
        xmlbo = "4321"
    define_macros = [
        ('XML_NS', '1'),
        ('XML_DTD', '1'),
        ('BYTEORDER', xmlbo),
        ('XML_CONTEXT_BYTES','1024'),
        ]
    if sys.platform == "win32":
        # HAVE_MEMMOVE is not in PC/pyconfig.h
        define_macros.extend([
         ('HAVE_MEMMOVE', '1'),
         ('XML_STATIC', ''),
        ])
    include_dirs = ['extensions/expat/lib']
    sources.extend([
        'extensions/expat/lib/xmlparse.c',
        'extensions/expat/lib/xmlrole.c',
        'extensions/expat/lib/xmltok.c',
        ])
    libraries = []
    library_dirs = []

config_h = get_config_h_filename()
config_h_vars = parse_config_h(open(config_h))
for feature_macro in ['HAVE_MEMMOVE', 'HAVE_BCOPY']:
    if config_h_vars.has_key(feature_macro):
        define_macros.append((feature_macro, '1'))

ext_modules.append(
    Extension(xml('.parsers.pyexpat'),
              define_macros=define_macros,
              include_dirs=include_dirs,
              library_dirs=library_dirs,
              libraries=libraries,
              extra_link_args=LDFLAGS,
              sources=sources
              ))

# Build sgmlop
ext_modules.append(
    Extension(xml('.parsers.sgmlop'),
              extra_link_args=LDFLAGS,
              sources=['extensions/sgmlop.c'],
              ))

# Build boolean
ext_modules.append(
    Extension(xml('.utils.boolean'),
              extra_link_args=LDFLAGS,
              sources=['extensions/boolean.c'],
              ))


# On Windows, install the documentation into a directory xmldoc, along
# with xml/_xmlplus. For RPMs, docs are installed into the RPM doc
# directory via setup.cfg (usuall /usr/doc). On all other systems, the
# documentation is not installed.

doc2xmldoc = 0
if sys.platform == 'win32':
    doc2xmldoc = 1

# This is a fragment from MANIFEST.in which should contain all
# files which are considered documentation (doc, demo, test, plus some
# toplevel files)

# distutils 1.0 has a bug where
# recursive-include test/output test_*
# is translated into a pattern ^test\\output\.*test\_[^/]*$
# on windows, which results in files not being included. Work around
# this bug by using graft where possible.
docfiles="""
recursive-include doc *.html *.tex *.txt *.gif *.css *.api *.web

recursive-include demo README *.py *.xml *.dtd *.html *.htm
include demo/genxml/data.txt
include demo/dom/html2html
include demo/xbel/doc/xbel.bib
include demo/xbel/doc/xbel.tex
include demo/xmlproc/catalog.soc

recursive-include test *.py *.xml *.html *.dtd
include test/test.xml.out
graft test/output

include ANNOUNCE CREDITS LICENCE README* TODO

global-exclude */CVS/*
"""

if doc2xmldoc:
    xmldocfiles = [
        Data_Files(copy_to = 'xmldoc',
                   template = string.split(docfiles,"\n"),
                   preserve_path = 1)
        ]
else:
    xmldocfiles = []

setup (name = "PyXML",
       version = "0.8.4", # Needs to match xml/__init__.version_info
       description = "Python/XML package",
       author = "XML-SIG",
       author_email = "xml-sig@python.org",
       url = "http://www.python.org/sigs/xml-sig/",
       long_description =
"""XML Parsers and API for Python
This version of PyXML was tested with Python 2.x.
""",

       # Override certain command classes with our own ones
       cmdclass = {'install_data':install_Data_Files,
                   'bdist_wininst':wininst_request_delete
                   },

       package_dir = {xml(''):'xml'},

       data_files = [Data_Files(base_dir='install_lib',
                                copy_to=xml('/dom/de/LC_MESSAGES'),
                                files=['xml/dom/de/LC_MESSAGES/4Suite.mo']),
                     Data_Files(base_dir='install_lib',
                                copy_to=xml('/dom/en_US/LC_MESSAGES'),
                                files=['xml/dom/en_US/LC_MESSAGES/4Suite.mo']),
                     Data_Files(base_dir='install_lib',
                                copy_to=xml('/dom/fr/LC_MESSAGES'),
                                files=['xml/dom/fr/LC_MESSAGES/4Suite.mo']),
                     ] + xmldocfiles,
       
       packages = [xml(''), 
                   xml('.dom'), xml('.dom.html'), xml('.dom.ext'),
                   xml('.dom.ext.reader'),
                   xml('.marshal'), xml('.unicode'),
                   xml('.parsers'), xml('.parsers.xmlproc'),
                   xml('.sax'), xml('.sax.drivers'),
                   xml('.sax.drivers2'), xml('.utils'), xml('.schema'),
                   #xml('.xpath'), xml('.xslt')
                   ] + extra_packages,

       ext_modules = ext_modules,

       scripts = ['scripts/xmlproc_parse', 'scripts/xmlproc_val']
       )
