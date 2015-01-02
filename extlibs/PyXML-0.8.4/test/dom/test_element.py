from TestSuite import EMPTY_NAMESPACE
def get_exception_name(code):
    import types
    from xml import dom
    for (name,value) in vars(dom).items():
        if (type(value) == types.IntType
        and value == code):
            return name

def test(tester):

    tester.startGroup('Element')

    tester.startTest('Testing syntax')
    try:
        from xml.dom import Element
        from xml.dom.Element import Element
    except:
        tester.tester.error('Error in syntax', 1)
    tester.testDone()


    tester.startTest('Creating test environment')
    from xml.dom import DOMException
    from xml.dom import INVALID_CHARACTER_ERR
    from xml.dom import WRONG_DOCUMENT_ERR
    from xml.dom import INUSE_ATTRIBUTE_ERR
    from xml.dom import NOT_FOUND_ERR
    from xml.dom import NO_MODIFICATION_ALLOWED_ERR
    from xml.dom import implementation

    dt = implementation.createDocumentType('','','')
    doc = implementation.createDocument(EMPTY_NAMESPACE,'ROOT',dt)

    doc_nons = implementation.createDocument(EMPTY_NAMESPACE,'ROOT',dt)

    ns = 'www.fourthought.com'
    e_ns = doc.createElementNS(ns, 'TEST')
    e = doc.createElement('TEST')
    tester.testDone()


    tester.startTest('Testing attributes')
    if e.tagName != 'TEST':
        tester.error("tagName failed")
    try:
        e.tagName = "test"
    except DOMException, exc:
        if exc.code != NO_MODIFICATION_ALLOWED_ERR:
            tester.error('Wrong exception on read-only violation')
    tester.testDone()


    tester.startTest('Testing setAttribute()')
    if e.setAttribute('Attr1','Value 1') != None:
        tester.error('setAttribvute returns a value')

    if e.attributes.length != 1:
        tester.error('setAttribute did not add the attribute')

    e.setAttribute('Attr1','Value 2');
    if e.attributes.length != 1:
        tester.error('setAttribute did not replace the attribute')

    try:
        e.setAttribute('A<ttr','Value3')
    except DOMException , x:
        if x.code != INVALID_CHARACTER_ERR:
            tester.error('Wrong exception on illegal character')
    else:
        tester.error('setAttribute allowed illegal characters')
    tester.testDone()


    tester.startTest('Testing getAttribute()')
    if e.getAttribute('Attr1') != 'Value 2':
        tester.error('getAttribute returned the worng string')

    if e.getAttribute('Attr2') != '':
        tester.error('getAttribute returns value for non-existant attribute')
    tester.testDone()


    tester.startTest('Testing hasAttribute()')
    if not e.hasAttribute('Attr1'):
        tester.error('hasAttribute didn\'t find the attribute')

    if e.hasAttribute('Attr2'):
        tester.error('hasAttribute found a non-existant attribute')
    tester.testDone()


    tester.startTest('Testing removeAttribute()')
    if e.removeAttribute('Attr1') != None:
        tester.error('removeAttribute returns something')
    if e.attributes.length != 0:
        tester.error('removeAttribute did not remove it')
    tester.testDone()


    tester.startTest('Testing setAttributeNode()')
    a = doc.createAttribute('attrNode1');

    if e.setAttributeNode(a) != None:
        tester.error('setAttributeNode returns a value')

    a1 = doc.createAttribute('attrNode1')
    if e.setAttributeNode(a1).nodeName != a.nodeName:
        tester.error('setAttribute does not return the replaced value')
    tester.testDone()


    tester.startTest('Testing getAttributeNode()')
    if e.getAttributeNode('attrNode1').nodeName != a1.nodeName:
        tester.error('getAttributeNode does not return the correct value')

    if e.getAttributeNode('attrNode2') != None:
        tester.error('getAttributeNode returns a value when it shouldn;t')
    tester.testDone()


    tester.startTest('Testing removeAttributeNode()')
    if e.removeAttributeNode(a1).nodeName != a1.nodeName:
        tester.error('removeAttributeNode does not return the correct value')

    if e.attributes.length != 0:
        tester.error('removeAttributeNode does not actually remove it')

    a2 = doc.createAttribute('attrNode2')
    try:
        e.removeAttributeNode(a2)
    except DOMException, x:
        if x.code != NOT_FOUND_ERR:
            raise x
    tester.testDone()


    tester.startTest('Testing getElementsByTagName()')
    e2 = doc.createElement('TAG1')
    e3 = doc.createElement('TAG1')
    e4 = doc.createElement('TAG2')
    e5 = doc.createElement('TAG3')

    e.appendChild(e2);
    e2.appendChild(e3);
    e.appendChild(e4);
    e2.appendChild(e5);

    tagList = e.getElementsByTagName('TAG1')

    if tagList.length != 2:
        tester.error('getElementsByTagName returned the worng number')

    tagList = e.getElementsByTagName('*')

    if tagList.length != 4:
        tester.error('getElementsByTagName(*) returned the wrong number');
    tester.testDone()


    tester.startTest('Testing setAttributeNS()')
    if e.setAttributeNS('www.fourthought.com','ft:Attr1','Value 1') != None:
        tester.error('setAttributeNS returns a value')
    if e.attributes.length != 1:
        tester.error('setAttributeNS did not add the attribute')
    e.setAttributeNS('www.fourthought.com','ft:Attr1','Value 2')
    if e.attributes.length != 1:
        tester.error('setAttributeNS did not replace the attribute')
    try:
        e.setAttributeNS('www.fourthought.com','ft:Attr<2>','Value3')
    except DOMException , x:
        if x.code != INVALID_CHARACTER_ERR:
            tester.error('Wrong exception on illegal character: %s' % str(x.code))
    else:
        tester.error('setAttributeNS allowed illegal characters')
    tester.testDone()


    tester.startTest('Testing getAttributeNS()')
    if e.getAttributeNS('www.fourthought.com','Attr1') != 'Value 2':
        tester.error('getAttributeNS returned the worng string')

    if e.getAttributeNS('www.fourthought.com','Attr2') != '':
        tester.error('getAttributeNS returns value for non-existant attribute')
    tester.testDone()


    tester.startTest('Testing hasAttributeNS()')
    if not e.hasAttributeNS('www.fourthought.com','Attr1'):
        tester.error('hasAttributeNS didn\'t find the attribute')

    if e.hasAttributeNS('www.fourthought.com','Attr2'):
        tester.error('hasAttributeNS found a non-existant attribute')
    tester.testDone()


    tester.startTest('Testing removeAttributeNS()')
    if e.removeAttributeNS('www.fourthought.com','Attr1') != None:
        tester.error('removeAttributeNS returns something')
    if e.attributes.length != 0:
        tester.error('removeAttributeNS did not remove it')
    tester.testDone()


    tester.startTest('Testing setAttributeNodeNS()')
    attr = doc.createAttributeNS('www.fourthought.com','ft:ns1')
    attr.value = 'TEST'
    if e.setAttributeNodeNS(attr) != None:
        tester.error('setAttributeNodeNS returns a value')

    attr1 = doc.createAttributeNS('www.fourthought.com','ft:ns1')
    if e.setAttributeNodeNS(attr1).nodeName != attr.nodeName:
        tester.error('setAttributeNS does not return the replaced value')
    tester.testDone()


    tester.startTest('Testing getAttributeNodeNS()')
    if e.getAttributeNodeNS('www.fourthought.com', 'ns1').nodeName != attr1.nodeName:
        tester.error('getAttributeNodeNS does not return the correct value')

    if e.getAttributeNodeNS('www.fourthought.com','ns2') != None:
        tester.error('getAttributeNodeNS returns a value when it shouldn;t')
    tester.testDone()


    tester.startTest('Testing getElementsByTagNameNS()')
    eNs = doc.createElementNS('www.fourthought.com','ft:ns')
    e.appendChild(eNs)

    rt = e.getElementsByTagNameNS('www.fourthought.com','ns')
    if len(rt) != 1:
        tester.error('failed with specified namespace and localName')
    rt = e.getElementsByTagNameNS('www.fourthought.com','*')
    if len(rt) != 1:
        tester.error('failed with specified namespace and * localName')
    rt = e.getElementsByTagNameNS('*','ns')
    if len(rt) != 1:
        print rt
        tester.error('failed with * namespace and specified localName')
    rt = e.getElementsByTagNameNS('*','*')
    if len(rt) != 5:
        print rt
        tester.error('failed with * namespace and localName')
    tester.testDone()


    tester.startTest('Testing ext.ReleaseNode()')
    from xml.dom import ext
    ext.ReleaseNode(e)

    if e.childNodes.length != 0:
        tester.error('ReleaseNode did not remove from parent')

    if e5.parentNode != None:
        tester.error('ReleaseNode did not set parent to None')
    tester.testDone()


    tester.startTest('Test cloneNode()')
    e.setAttribute('ATT1','VALUE 1')
    e6 = e.cloneNode(1)

    if e.attributes.length != e6.attributes.length:
        tester.error("cloneNode didn't do the right number of attributes")

    a1 = e.attributes.item(0)
    a2 = e6.attributes.item(0)
    if a1.name != a2.name:
        tester.error('cloneNode did not copy the attribute names')

    if a1.value != a2.value:
        tester.error('cloneNode did not copy the attribute values')

    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
