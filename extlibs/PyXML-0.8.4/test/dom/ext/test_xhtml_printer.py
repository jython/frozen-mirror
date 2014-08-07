def test(stream):
    from xml.dom.ext.reader import HtmlLib

    doc = HtmlLib.FromHtmlStream(stream)

    from xml.dom import ext

    #print "Not Pretty"
    #ext.XHtmlPrint(doc)

    print "Pretty"
    ext.XHtmlPrettyPrint(doc)



if __name__ == '__main__':
    import sys
    test(sys.stdin)
