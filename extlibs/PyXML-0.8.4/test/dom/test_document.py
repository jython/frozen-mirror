from TestSuite import EMPTY_NAMESPACE
def test(tester):
    tester.startGroup('Document')

    tester.startTest('Checking syntax')
    try:
        from xml.dom import Document
        from xml.dom.Document import Document
    except:
        tester.error('Error in syntax' ,1)
    tester.testDone()


    tester.startTest('Creating test environment')
    from xml.dom import implementation
    from xml.dom import DOMException
    from xml.dom import INVALID_CHARACTER_ERR
    from xml.dom import NOT_SUPPORTED_ERR
    from xml.dom import HIERARCHY_REQUEST_ERR

    dt = implementation.createDocumentType('','','')
    doc = implementation.createDocument(EMPTY_NAMESPACE,None,dt);
    tester.testDone()


    tester.startTest('Testing ownerDocument')
    if doc.ownerDocument.nodeName != doc.nodeName:
        tester.error('ownerDocument failed')
    tester.testDone()


    tester.startTest('Testing createElement()')
    e = doc.createElement('ELEMENT')
    if e.ownerDocument.nodeName != doc.nodeName:
        tester.error('createElement does not set ownerDocument')
    if e.tagName != 'ELEMENT':
        tester.error('createElement does not set tagName')
    try:
        e2 = doc.createElement('BAD<NAME');
    except DOMException, data:
        if data.code != INVALID_CHARACTER_ERR:
            tester.error('createElement throws wrong exception')
    else:
        tester.error('createElement does not catch illegal characters')
    tester.testDone()


    tester.startTest('Testing documentElement')
    doc.appendChild(e)
    if doc.documentElement.nodeName != e.nodeName:
        tester.error('documentElement does not set properly')
    doc.removeChild(e)
    if doc.documentElement != None:
        tester.error('documentElement returns an element when there is none')
    tester.testDone()


    tester.startTest('Testing createDocumentFragment()')
    df = doc.createDocumentFragment()
    if df.ownerDocument.nodeName != doc.nodeName:
        tester.error('createDocumentFragment does not set ownerDocument')
    tester.testDone()


    tester.startTest('Testing createTextNode()')
    t = doc.createTextNode('TEXT')
    if t.data != 'TEXT':
        tester.error('createTextNode does not set data')
    if t.ownerDocument.nodeName != doc.nodeName:
        tester.error('createTextNode does not set ownerDocument')
    tester.testDone()


    tester.startTest('Testing createComment()')
    c = doc.createComment('COMMENT')
    if c.data != 'COMMENT':
        tester.error('createComment does not set data');
    if c.ownerDocument.nodeName != doc.nodeName:
        tester.error('createComment does not set ownerDocument')
    tester.testDone()


    tester.startTest('Testing createCDATASection()')
    cd = doc.createCDATASection('CDATA')
    if cd.data != 'CDATA':
        tester.error('createCDATASection does not set data')
    if cd.ownerDocument.nodeName != doc.nodeName:
        tester.error('createCDATASEction does not set ownerDocument');
    tester.testDone()


    tester.startTest('Testing createProcessingInstruction()')
    pi = doc.createProcessingInstruction('TARGET','DATA');
    if pi.target != 'TARGET':
        tester.error('createProcessingInstruction does not set target');
    if pi.data != 'DATA':
        tester.error('createProcessingInstruction does not set data');
    if pi.ownerDocument.nodeName != doc.nodeName:
        tester.error('createProcessingInstruction does not set ownerDocument');
    try:
        tester.pi2 = doc.createProcessingInstruction('BAD<NAME','DATA');
    except DOMException, data:
        if data.code != INVALID_CHARACTER_ERR:
            tester.error('createProcessingInstruction throws wrong exception for illegal characters')
    else:
        tester.error('createProcessingInstruction does not catch illegal characters')
    tester.testDone()


    tester.startTest('Testing createAttribute()')
    a = doc.createAttribute('ATTRIBUTE');
    if a.ownerDocument.nodeName != doc.nodeName:
        tester.error('createAttribute does not set the owner document')
    if a.name != 'ATTRIBUTE':
        tester.error('createAttribute does not set the name')
    if a.localName != None:
        tester.error('createAttribute sets the localName; should be (null)')
    if a.prefix != None:
        tester.error('createAttribute sets the prefix; should be (null)')
    if a.namespaceURI != None:
        tester.error('createAttribute sets the namespaceURI; should be (null)')
    try:
        a2 = doc.createAttribute('BAD<NAME');
    except DOMException, data:
        if data.code != INVALID_CHARACTER_ERR:
            tester.error('createAttribute throws wrong exception for illegal characters')
    else:
        tester.error('createAttribute does not catch illegal characters')
    tester.testDone()


    tester.startTest('Testing createEntityReference()')
    er = doc.createEntityReference('NAME')
    if er.ownerDocument.nodeName != doc.nodeName:
        tester.error('createEntityReference does not set owner document')
    if er.nodeName != 'NAME':
        tester.error('createEntityReference does not set name')
    try:
        er2 = doc.createEntityReference('BAD<NAME')
    except DOMException, data:
        if data.code != INVALID_CHARACTER_ERR:
            tester.error('createEntityReference throws wrong exception for illegal characters')
    else:
        tester.error('createEntityReference does not catch illegal characters')
    tester.testDone()


    tester.startTest('Testing getElementsByTagName()')
    e1 = doc.createElement('SUB1');
    e2 = doc.createElement('SUB2');
    e3 = doc.createElement('SUB2');

    # XML string '<ELEMENT><SUB1><SUB2/></SUB1><SUB2/></ELEMENT>'
    e1.appendChild(e2)
    e.appendChild(e1)
    e.appendChild(e3)
    doc.appendChild(e)

    nl = doc.getElementsByTagName('ELEMENT');
    if nl.length != 1:
        tester.error('getElementsByTagName does not return root element')

    nl = doc.getElementsByTagName('SUB2')
    if nl.length != 2:
        tester.error('getElementsByTagName failed to search the tree')

    nl = doc.getElementsByTagName('*');
    if nl.length != 4:
        tester.error('getElementsByTagName does not get all elements');
    tester.testDone()


    tester.startTest('Testing cloneNode()')
    doc2 = doc.cloneNode(1)
    ret = RecursiveCompare(doc.documentElement, doc2.documentElement)
    if ret[0]:
        tester.error('cloneNode '+ret[1])
    tester.testDone()


    tester.startTest('Testing importNode()')
    imp = doc2.importNode(e,1)
    if imp.parentNode != None:
        tester.error('importNode did not reset parentNode')
    if imp.ownerDocument != doc2:
        tester.error('importNode did not set ownerDocument')
    tester.testDone()


    tester.startTest('Testing appendChild() with a DocumentFragment')
    c1 = doc.createComment('C1')
    c2 = doc.createComment('C2')
    c3 = doc.createComment('C3')
    c4 = doc.createComment('C4')
    df.appendChild(c1)
    df.appendChild(c2)
    df.appendChild(c3)
    doc.appendChild(df)
    if df.childNodes.length != 0:
        tester.error('Appending does not remove all the children')
    if doc.childNodes.length != 5:
        tester.error('Appending does not add all the children')
    tester.testDone()


    tester.startTest('Testing insertBefore() with a DocumentFragment')
    doc.removeChild(c3)
    doc.removeChild(c2)

    df.appendChild(c2)
    df.appendChild(c3)
    df.appendChild(c4)
    doc.insertBefore(df,c1)
    if doc.childNodes[2].data != c2.data:
        tester.error('insertBefore failed to place children in proper order')
    if doc.lastChild.data != c1.data:
        tester.error('insertbefore failed to place children in proper order')
    if doc.childNodes.length != 6:
        tester.error('insertBefore failed to add all of the children')
    tester.testDone()


    tester.startTest('Testing replaceChild() with a DocumentFragment')
    doc.removeChild(c1)
    doc.removeChild(c2)
    doc.removeChild(c3)

    df.appendChild(c1)
    df.appendChild(c2)
    df.appendChild(c3)
    doc.replaceChild(df,c4)
    if doc.childNodes.length != 5:
        tester.error('replaceChild does not add all the children')
    if doc.childNodes[2].data != c1.data:
        tester.error('replaceChild failed to place children in proper order')
    if doc.lastChild.data != c3.data:
        tester.error('replaceChild failed to place children in proper order')
    tester.testDone()


    tester.startTest('Testing overridden appendChild()')
    e.removeChild(e1)
    e.removeChild(e3)
    e1.removeChild(e2)
    try:
        doc.appendChild(e1)
    except DOMException, data:
        if data.code != HIERARCHY_REQUEST_ERR:
            tester.error('appendChild throws wrong exception')
    else:
        tester.error('appendChild allows two elements')
    tester.testDone()


    tester.startTest('Testing overridden insertBefore()')
    try:
        doc.insertBefore(e1,e)
    except DOMException, data:
        if data.code != HIERARCHY_REQUEST_ERR:
            print data
            tester.error('insertBefore throws wrong exception')
    else:
        tester.error('insertBefore allows two elements')
    tester.testDone()


    tester.startTest('Testing overridden replaceChild()')
    doc.replaceChild(e1,e)
    if doc.documentElement.nodeName != e1.nodeName:
        tester.error('replaceChild did not set documentElement correctly');
    try:
        doc.replaceChild(e,c1)
    except DOMException, data:
        if data.code != HIERARCHY_REQUEST_ERR:
            tester.error('replaceChild throws wrong exception')
    else:
        tester.error('replaceChild allows two elements')
    tester.testDone()


    tester.startTest('Testing createElementNS()')
    e = doc.createElementNS('www.fourthought.com','ft:ns')
    if e.nodeName != 'ft:ns':
        tester.error('createElementNS does not set nodeName')
    if e.tagName != 'ft:ns':
        tester.error('createElementNS does not set tagName')
    if e.namespaceURI != 'www.fourthought.com':
        tester.error('createElementNS does not set namespaceURI')
    if e.prefix != 'ft':
        tester.error('createElementNS does not set prefix')
    if e.localName != 'ns':
        tester.error('createElementNS does not set localName')
    tester.testDone()


    tester.startTest('Testing createAttributeNS()')
    a = doc.createAttributeNS('www.fourthought.com','ft:ans')
    e.setAttributeNodeNS(a)
    if a.nodeName != 'ft:ans':
        tester.error('createAttributeNS does not set nodeName')
    if a.name != 'ft:ans':
        tester.error('createAttributeNS does not set name')
    if a.namespaceURI != 'www.fourthought.com':
        tester.error('createAttributeNS does not set namespaceURI')
    if a.prefix != 'ft':
        tester.error('createAttributeNS does not set prefix')
    if a.localName != 'ans':
        tester.error('createAttributeNS does not set localName')
    tester.testDone()


    tester.startTest('Testing getElementsByTagNameNS()')
    e1 = doc.createElementNS('www.fourthought.com','ft:ns1')
    e2 = doc.createElementNS('www.fourthought.com','ft:ns2')
    e3 = doc.createElementNS('www.fourthought.com','ft:ns2')

    # XML string '<ELEMENT><SUB1><SUB2/></SUB1><SUB2/></ELEMENT>'
    e1.appendChild(e2)
    e.appendChild(e1)
    e.appendChild(e3)
    doc.documentElement.appendChild(e)

    nl = doc.getElementsByTagNameNS('www.fourthought.com','ns')
    if nl.length != 1:
        tester.error('getElementsByTagNameNS does not return root element')

    nl = doc.getElementsByTagNameNS('www.fourthought.com','ns2')
    if nl.length != 2:
        tester.error('getElementsByTagNameNS failed to search the tree')

    nl = doc.getElementsByTagName('*');
    if nl.length != 5:
        tester.error('getElementsByTagNameNS does not get all elements');
    tester.testDone()


    return 1


def RecursiveCompare(old, new):
    if old.nodeName != new.nodeName:
        return (1, 'did not copy names')
    if old.nodeValue != new.nodeValue:
        return (1, 'did not copy values')
    if old.ownerDocument == new.ownerDocument:
        return (1, 'did not change ownerDocument')
    if old.childNodes.length != new.childNodes.length:
        return (1, 'did not copy all children')
    for i in range(old.childNodes.length):
        ret = RecursiveCompare(old.childNodes[i], new.childNodes[i])
        if ret[0]:
            return ret
    return (0, 'passed')


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
