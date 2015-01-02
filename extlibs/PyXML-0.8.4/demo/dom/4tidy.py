import sys, cStringIO
from xml.dom.ext.reader import HtmlLib
from xml.dom.ext import XHtmlPrint

def Tidy(doc):
    #stream = cStringIO.StringIO()
    #XHtmlPrint(doc, stream=stream)
    #text = stream.getvalue()

    XHtmlPrint(doc)
    return


if __name__ == "__main__":
    html_reader = HtmlLib.Reader()
    if len(sys.argv) == 3:
        uri = sys.argv[1]
        encoding = sys.argv[2]
    elif len(sys.argv) == 2:
        uri = sys.argv[1]
        encoding = ''
    else:
        print "%s requires one or two arguments: the first is a URL or file name to be tidied.  The optional second is the encoding to assume for the input."%sys.argv[0]
        sys.exit(-1)

    html_doc = html_reader.fromUri(uri, charset=encoding)
    Tidy(html_doc)
