def test(inFile):

    from xml.dom.ext.reader import HtmlLib
    from xml.dom import ext
    from xml.dom import Node
    from xml.dom.html import HTMLDocument



    doc = HTMLDocument.HTMLDocument()

    HtmlLib.FromHtmlStream(inFile,doc)

    print doc

    ext.PrettyPrint(doc)




if __name__ == '__main__':

    import sys
    inFile = sys.stdin
    if len(sys.argv) == 2:
        inFile = open(sys.argv[1],'r')

    test(inFile)
