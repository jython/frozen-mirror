"""
Classes to store bookmarks and dump them to XBEL.
"""

import sys,string,types
from xml.sax.saxutils import escape

# --- Class for bookmark container

class Bookmarks:

    def __init__(self, info=None, id=None, title=None):
        self.folders=[]
        self.folder_stack=[]
        self.desc = "No description"
        self.info = info
        self.id = id
        self.title = title

    def add_folder(self, name, added=None):
        nf=Folder(name, added)
        if self.folder_stack==[]:
            self.folders.append(nf)
        else:
            self.folder_stack[-1].add_child(nf)

        self.folder_stack.append(nf)
        return nf

    def add_bookmark(self,name=None,
                     added=None, visited=None, modified=None,
                     href=None, desc = None):
        nb=Bookmark(name,added,visited,modified,href, desc = desc)

        if self.folder_stack!=[]:
            self.folder_stack[-1].add_child(nb)
        else:
            self.folders.append(nb)
        return nb

    def add_separator(self):
        s = Separator()
        if self.folder_stack!=[]:
            self.folder_stack[-1].add_child(s)
        else:
            self.folders.append(s)
        return s

    def leave_folder(self):
        if self.folder_stack!=[]:
            del self.folder_stack[-1]

    def update_ids(self):
        ids = {}
        aliases = []
        for folder in self.folders:
            folder.update_ids(ids, aliases)
        for alias in aliases:
            alias.update_link(ids)

    def dump_xbel(self,out=sys.stdout):
        if self.id:
            ID = ' id="%s"' % self.id
        else:
            ID = ""
        out.write('<?xml version="1.0"?>\n'
                  '<!DOCTYPE xbel PUBLIC "+//IDN python.org//DTD XML Bookmark Exchange Language 1.1//EN//XML" "http://pyxml.sourceforge.net/topics/dtds/xbel-1.1.dtd">\n'
                  '<xbel%s>\n'
                  % ID
        )
        if self.title:
            out.write("  <title>%s</title>\n" % esc_enc(self.title))
        if self.info:
            out.write("  <info>%s</info>\n" % esc_enc(self.info))
        out.write("  <desc>%s</desc>\n" % (esc_enc(self.desc),) )

        for folder in self.folders:
            folder.dump_xbel(out)
        out.write("</xbel>\n")

    def dump_adr(self,out=sys.stdout):
        out.write("Opera Hotlist version 2.0\n\n")
        for folder in self.folders:
            folder.dump_adr(out)

    def dump_netscape(self,out=sys.stdout):
        out.write("<!DOCTYPE NETSCAPE-Bookmark-file-1>\n")
        out.write("<!-- This is an automatically generated file.\n")
        out.write("It will be read and overwritten.\n")
        out.write("Do Not Edit! -->\n")
        # Mozilla recognizes the content-type declaration; let's hope
        # Netscape 4 is not bothered by it
        out.write('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n')
        if self.title:
            out.write("<TITLE>" + esc_enc(self.title) + "</TITLE>\n")
        else:
            out.write("<TITLE>Bookmarks</TITLE>\n")
        out.write("<H1>" + esc_enc(self.desc) + "</H1>\n\n")

        out.write("<DL><p>\n")
        for folder in self.folders:
            folder.dump_netscape(out)
        out.write("</DL><p>\n")

    # Lynx uses multiple bookmark files; each folder will be written to a
    # different file.
    def dump_lynx(self, path):
        import os
        for folder in self.folders:
            # First, figure out a reasonable filename for this folder
            filename = string.replace(folder.title, ' ', '_') + '.html'

            # Open a file for the top-level folders
            output = open( os.path.join(path, filename), 'w')
            print 'folder title:', folder.title, filename
            output.write('<head>\n<title>%s</title>\n<head>\n'
                         % (folder.title,) )
            output.write('<p>\n<ol>\n')

            folder.dump_lynx(output)

            output.close()

# --- Superclass for folder and bookmarks

class Node:
    def __init__(self, name, added=None,
                 visited=None, modified=None, id=None, desc=None):
        self.title = name
        self.added = added
        self.visited = visited
        self.modified = modified
        self.id = id
        self.desc = desc

    def update_ids(self, ids, aliases):
        if self.id:
            while ids.has_key(self.id):
                # Duplicate ID
                self.id = self.id + '0'
            ids[self.id] = self

    def gen_id(self, ids):
        self.id = 'X'+str(id(self))
        self.update_ids(ids, [])

# --- Class for folders

class Folder(Node):

    def __init__(self, name, added = None, info = None, id=None,
                 folded = 'yes', icon = None, toolbar = 'no', desc=None):
        Node.__init__(self, name, added=added, id=None,desc=desc)
        self.children=[]
        self.info = None
        self.folded = None
        self.icon = None
        self.toolbar = None

    def add_child(self,child):
        self.children.append(child)

    def update_ids(self, ids, aliases):
        Node.update_ids(self, ids, aliases)
        for node in self.children:
            node.update_ids(ids, aliases)

    def is_folded(self):
        # folded defaults to yes
        return self.folded is None or self.folded == 'yes'

    def dump_xbel(self,out):
        if self.id:
            ID = ' id="%s"' % self.id
        else:
            ID = ""
        if self.added:
            added = ' added="%s"' % self.added
        else:
            added = ""
        if self.folded is not None:
            folded = ' folded="%s"' % self.folded
        else:
            folded = ""
        if self.icon is not None:
            icon = ' icon="%s"' % self.icon
        else:
            icon = ""
        if self.toolbar is not None:
            toolbar = ' toolbar="%s"' % self.toolbar
        else:
            toolbar = ""
        
        out.write("  <folder%s%s%s%s%s>\n" % (ID, added, folded, icon, toolbar))
        out.write("    <title>%s</title>\n" % esc_enc(self.title) )
        if self.info:
            out.write("    <info>%s</info>\n" % esc_enc(self.info))
        if self.desc:
            out.write("    <desc>%s</desc>\n" % esc_enc(self.desc))
        for child in self.children:
            child.dump_xbel(out)
        out.write("  </folder>\n")

    def dump_adr(self,out):
        out.write("#FOLDER\n")
        out.write("\tNAME=%s\n" % self.title)
        out.write("\tADDED=%s\n" % "0 (?)")
        out.write("\tVISITED=%s\n" % "0 (?)")
        out.write("\tORDER=-1\n")
        out.write("\n")

        for child in self.children:
            child.dump_adr(out)

        out.write("\n")
        out.write("-\n")

    def dump_netscape(self,out):
        if self.id:
            ID = ' ID="%s"' % self.id
        else:
            ID = ""        
        if self.is_folded():
            folded = " FOLDED"
        else:
            folded = ""
        if self.added:
            added = ' ADD_DATE="%s"' % self.added
        else:
            added = ""
        out.write("  <DT><H3%s%s%s>%s</H3>\n" %
                  (folded,added,ID,esc_enc(self.title)))
        if self.desc:
            out.write("  <DD>%s\n" %
                      (esc_enc(self.desc)))
            
        out.write("  <DL><p>\n")

        for child in self.children:
            child.dump_netscape(out)

        out.write("  </DL><p>\n")

    def dump_lynx(self, out):
        out.write("  <H3>%s</H3>\n" % self.title)
        out.write("  <OL>\n")

        for child in self.children:
            child.dump_lynx(out)

        # Mustn't write the closing </OL>, because Lynx will add it
        # when it reads the bookmark file.
        ##out.write("  </OL>\n")

# --- Class for bookmarks

class Bookmark(Node):

    def __init__(self, name, added=None, visited=None,
                 modified=None, href=None, info=None, id = None, desc = None):
        Node.__init__(self,name,added,visited,modified, id=id, desc=desc)
        self.href = href
        self.info = info

    def dump_xbel(self,out):
        if self.id:
            ID = ' id="%s"' % self.id
        else:
            ID = ""
        if self.visited!=None:
            visited = ' visited="%s"' % escape(self.visited)
        else:
            visited = ""

        if self.added!=None:
            added = ' added="%s"' % escape(self.added)
        else:
            added = ""

        if self.modified!=None:
            modified = ' modified="%s"' % escape(self.modified)
        else:
            modified = ""

        out.write('    <bookmark href="%s"%s%s%s%s>\n' %
                  ( esc_enc(self.href), ID, added, visited, modified) )
        out.write("      <title>%s</title>\n" % esc_enc(self.title) )
        if self.info:
            out.write("    <info>%s</info>\n" % esc_enc(self.info))
        if self.desc:
            out.write("    <desc>%s</desc>\n" % esc_enc(self.desc))
        out.write("    </bookmark>\n")

    def dump_adr(self,out):
        out.write("#URL\n")
        out.write("\tNAME=%s\n" % self.title)
        out.write("\tURL=%s\n" % self.href)
        out.write("\tCREATED=%s\n" % "0 (?)")
        out.write("\tVISITED=%s\n" % "0 (?)")
        out.write("\tORDER=-1\n")
        out.write("\n")

    def dump_netscape(self,out):
        added = visited = modified = ""
        if self.added:
            added = ' ADD_DATE="%s"' % encode(self.added)
        if self.visited:
            visited = ' LAST_VISIT="%s"' % encode(self.visited)
        if self.modified:
            modified = ' LAST_MODIFIED="%s"' % encode(self.modified)
        out.write("    <DT><A HREF=\"%s\"%s%s%s>%s</A>\n" %
                  (encode(self.href),added,visited,modified,
                   esc_enc(self.title)))
        if self.desc:
            out.write("    <DD>%s\n" %(esc_enc(self.desc)))
    def dump_lynx(self, out):
        out.write("<LI><A HREF=\"%s\">%s</A>\n" % (self.href, esc_enc(self.title)) )

# --- Class for separators

class Separator(Node):
    def __init__(self):
        Node.__init__(self, None)
    
    def dump_xbel(self, out):
        out.write('    <separator/>\n')

    def dump_netscape(self, out):
        out.write("    <HR>\n")

# --- Class for separators

class InvalidReference(Exception):
    pass

class Alias(Node):
    def __init__(self, aliased_to):
        Node.__init__(self, None)
        if isinstance(aliased_to, Node):
            self.aliased_to = aliased_to
            self.ref = None
        else:
            self.aliased_to = None
            self.ref = aliased_to

    def update_ids(self, ids, aliases):
        aliases.append(self)

    def update_link(self, ids):
        if self.aliased_to:
            if self.aliased_to.id is None:
                self.aliased_to.gen_id(ids)
            self.ref = self.aliased_to.id
        else:
            try:
                self.aliased_to = ids[self.ref]
            except KeyError:
                raise InvalidReference, self.ref

    def dump_xbel(self, out):
        out.write('    <alias ref="%s">\n' % self.ref)

# --- helper functions

try:
    types.UnicodeType
except AttributeError:
    def encode(str, encoding = "utf-8"):
        # Can't do proper recoding in Python 1.5
        return str
else:
    def encode(str, encoding = "utf-8"):
        if type(str) == types.UnicodeType:
            return str.encode(encoding)
        return str

def esc_enc(str):
    return encode(escape(str))
