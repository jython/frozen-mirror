#! /usr/bin/env python
"""
%(program)s -- example script to convert comma-separated value file to
               XML using the Document Object Model (DOM), the Simple
               API for XML (SAX), or the 'write' model (a bunch of calls
               to <file>.write()).

Usage:  %(program)s [--dom|--sax|--write] [infile [outfile]]
"""
__version__ = '$Revision: 1.3 $'

import getopt
import os
import string
import sys

# Note that we only need one of these for any given version of the
# processing class.
#
from xml.dom.DOMImplementation import implementation
import xml.sax.writer
import xml.utils


def main():
    """Process command line parameters and run the conversion."""
    inpath = "-"
    outpath = "-"
    args = sys.argv[1:]
    processor_class = DOMProcess
    try:
        opts, args = getopt.getopt(args, "dhsw",
                                   ["dom", "help", "sax", "write"])
    except getopt.error, e:
        usage(err=e, rc=2)
    for opt, arg in opts:
        if opt in ("-d", "--dom"):
            processor_class = DOMProcess
        elif opt in ("-h", "--help"):
            usage()
        elif opt in ("-s", "--sax"):
            processor_class = SAXProcess
        elif opt in ("-w", "--write"):
            processor_class = WriteProcess
    if len(args) == 2:
        inpath, outpath = args
    elif len(args) == 1:
        inpath = args[0]
    elif len(args) == 0:
        pass
    else:
        usage(err="too many command-line arguments", rc=2)

    infp = get_input(inpath)
    outfp = get_output(outpath)

    processor = processor_class(infp, outfp)
    processor.run()

    infp.close()
    outfp.close()


class BaseProcess:
    """Base class for the conversion processors.  Each concrete subclass
    must provide the following methods:

    initOutput()
        Initialize the output stream and any internal data structures
        that the conversion process needs.

    addRecord(lname, fname, type)
        Add one record to the output stream (or the internal structures)
        where lname is the last name, fname is the first name, and type
        is either 'manager' or 'employee'.

    finishOutput()
        Finish all output generation.  If all work has been on internal
        data structures, this is where they should be converted to text
        and written out.
    """
    def __init__(self, infp, outfp):
        """Store the input and output streams for later use."""
        self.infp = infp
        self.outfp = outfp

    def run(self):
        """Perform the complete conversion process.

        This method is responsible for parsing the input and calling the
        subclass-provided methods in the right order.
        """
        self.initOutput()
        self.infp.readline()            # ignore field names
        rec = self.getNextRecord()
        while rec:
            lname, fname, type = rec
            self.addRecord(lname, fname, type)
            rec = self.getNextRecord()
        self.finishOutput()

    def getNextRecord(self):
        """Read and return the next input record, or return None."""
        line = self.infp.readline()
        if line:
            parts = map(string.strip, string.split(line, ','))
            lname, fname, eid, mid = parts
            type = ("employee", "manager")[eid == mid]
            return lname, fname, type
        else:
            return None


class DOMProcess(BaseProcess):
    """Concrete conversion process which uses a DOM structure as an
    internal data structure.

    Content is added to the DOM tree for each input record, and the
    entire tree is serialized and written to the output stream in the
    finishOutput() method.
    """
    def initOutput(self):
        # Create a new document with no namespace uri, qualified name,
        # or document type
        self.document = implementation.createDocument(None,None,None)
        self.personnel = self.document.createElement("personnel")
        self.document.appendChild(self.personnel)

    def addRecord(self, lname, fname, type):
        doc = self.document
        self.personnel.appendChild(doc.createTextNode("\n  "))
        emp = doc.createElement("employee")
        emp.setAttribute("type", type)
        self.personnel.appendChild(emp)
        emp.appendChild(doc.createTextNode("\n    "))
        ln = doc.createElement("lname")
        ln.appendChild(doc.createTextNode(lname))
        emp.appendChild(ln)
        emp.appendChild(doc.createTextNode("\n    "))
        fn = doc.createElement("fname")
        fn.appendChild(doc.createTextNode(fname))
        emp.appendChild(fn)
        emp.appendChild(doc.createTextNode("\n  "))

    def finishOutput(self):
        t = self.document.createTextNode("\n")
        self.personnel.appendChild(t)
        # XXX toxml not supported by 4DOM
        # self.outfp.write(self.document.toxml())
        xml.dom.ext.PrettyPrint(self.document, self.outfp)
        self.outfp.write("\n")


class SAXProcess(BaseProcess):
    """Concrete conversion process that uses a SAX implementation that
    writes output to a file.

    XML is generated by calling the SAX methods that would be called
    when the resulting document instance is parsed.  Data is written to
    the output stream incrementally with this approach, and no real
    internal state is maintained.
    """
    def initOutput(self):
        info = xml.sax.writer.XMLDoctypeInfo()
        info.add_element_container("personnel")
        info.add_element_container("employee")
        saxout = self.saxout = xml.sax.writer.PrettyPrinter(
            self.outfp, dtdinfo=info)
        saxout.startDocument()
        saxout.startElement("personnel", {})

    def addRecord(self, lname, fname, type):
        saxout = self.saxout
        saxout.startElement("employee", {"type": type})
        saxout.startElement("lname", {})
        saxout.characters(lname, 0, len(lname))
        saxout.endElement("lname")
        saxout.startElement("fname", {})
        saxout.characters(fname, 0, len(fname))
        saxout.endElement("fname")
        saxout.endElement("employee")

    def finishOutput(self):
        self.saxout.endElement("personnel")
        self.saxout.endDocument()


class WriteProcess(BaseProcess):
    """Concrete conversion process that simply formats the XML
    directly and uses the write() method of a file to write it out.

    The only helper function used to generate the XML is the
    xml.utils.escape() function; the methods of this class are
    solely responsible for proper formatting of the markup.
    """
    #
    # Note the simplicity of using a bunch of write() calls; using print
    # statements would also be reasonable in many contexts.
    #
    def initOutput(self):
        self.outfp.write('<?xml version="1.0" encoding="iso-8859-1"?>\n')
        self.outfp.write("<personnel>\n")

    def addRecord(self, lname, fname, type):
        self.outfp.write('  <employee type="%s">\n' % type)
        self.outfp.write("    <lname>%s</lname>\n" % xml.utils.escape(lname))
        self.outfp.write("    <fname>%s</fname>\n" % xml.utils.escape(fname))
        self.outfp.write("  </employee>\n")

    def finishOutput(self):
        self.outfp.write("</personnel>\n")


def get_input(path):
    """Get input file from path; '-' indicates stdin."""
    if path == "-":
        return sys.stdin
    else:
        return open(path)


def get_output(path):
    """Get output file from path; '-' indicates stdout."""
    if path == "-":
        return sys.stdout
    else:
        return open(path, "w")


def usage(err=None, rc=0):
    """Write out a usage message, possibly to stderr.

    If err or rc are true, the message is written to stderr instead of
    stdout.  The script docstring is used as the source of help text.
    Exits with result code rc.
    """
    if err or rc:
        sys.stdout = sys.stderr
    program = os.path.basename(sys.argv[0])
    if err:
        print "%s: %s" % (program, str(err))
    vars = {"program": program}
    print __doc__ % vars
    sys.exit(rc)


if __name__ == "__main__":
    main()
