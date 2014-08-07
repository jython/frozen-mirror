def error(msg):
    raise 'ERROR: ' + msg

from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')

    di = doc._get_implementation()
    doc2 = implementation.createHTMLDocument('The Title')
    import xml.dom.ext
    xml.dom.ext.PrettyPrint(doc2)
    return 1


if __name__ == '__main__':
    test()
