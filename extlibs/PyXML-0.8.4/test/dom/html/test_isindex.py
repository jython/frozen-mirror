from util import error
from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLIsIndexElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    i = doc.createElement('IsIndex')
    f = doc.createElement('Form')

    print 'testing get/set of Prompt'

    testAttribute(i,'prompt');
    print 'get/set Prompt works'

    print 'testing getForm'

    f.appendChild(i)

    if i._get_form().nodeName != f.nodeName:
        error('getForm failed')

    print 'getForm works'


if __name__ == '__main__':
    test()
