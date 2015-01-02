from TestSuite import EMPTY_NAMESPACE
from xml.dom import DOMException
from xml.dom import HIERARCHY_REQUEST_ERR
from xml.dom import WRONG_DOCUMENT_ERR
from xml.dom import NOT_FOUND_ERR

def get_exception_name(code):
    import types
    from xml import dom
    for (name,value) in vars(dom).items():
        if (type(value) == types.IntType
        and value == code):
            return name

def test(tester):

    tester.startGroup('Node')

    tester.startTest('Testing syntax')
    try:
        from xml.dom import Node
        from xml.dom.FtNode import FtNode
    except:
        tester.error('Error in syntax', 1)
    tester.testDone()


    tester.startTest('Creating the test environment')
    from xml.dom import implementation
    dt = implementation.createDocumentType('','','')
    doc = implementation.createDocument(EMPTY_NAMESPACE,'ROOT',dt);

    # We cannot use just plain old nodes, we need to use Elements
    p = doc.createElement('PARENT')

    nodes = []
    for ctr in range(3):
        n = doc.createElement('Child%d' % ctr)
        nodes.append(n)
    tester.testDone()


    tester.startTest("Testing attributes")
    if p.nodeName != 'PARENT':
        tester.error("Error getting nodeName");
    p.nodeValue = 'NodeValue';
    if p.nodeValue != 'NodeValue':
        tester.error('Error getting/setting nodeValue');
    if p.nodeType != Node.ELEMENT_NODE:
        tester.error('Error getting nodeType');
    if p.parentNode != None:
        tester.error('Error getting parentNode');
    p._4dom_setParentNode(None)
    if p.firstChild != None:
        tester.error('Error getting firstChild');
    if p.lastChild != None:
        tester.error('Error getting lastChild');
    if p.nextSibling != None:
        tester.error('Error getting nextSibling');
    if p.previousSibling != None:
        tester.error('Error getting previousSibling');
    if p.attributes == None:
        tester.error('Error getting attributes');
    if p.ownerDocument.nodeName != doc.nodeName:
        tester.error('Error getting ownerDocument');
    if p.namespaceURI != None:
        tester.error('Error getting namespaceURI')
    if p.prefix != None:
        tester.error('Error getting')
    if p.localName != None:
        tester.error('Error getting localName')
    tester.testDone()


    tester.startTest("Testing insertBefore()")
    if p.insertBefore(nodes[0],None).nodeName != nodes[0].nodeName:
        tester.error("Error inserting");

    if p.firstChild.nodeName != nodes[0].nodeName:
        tester.error("Error insert failed");
    if p.lastChild.nodeName != nodes[0].nodeName:
        tester.error("Error insert failed");

    if p.insertBefore(nodes[1],nodes[0]).nodeName != nodes[1].nodeName:
        tester.error("Error inserting");

    if p.firstChild.nodeName != nodes[1].nodeName:
        tester.error("Error insert failed");
    if p.lastChild.nodeName != nodes[0].nodeName:
        tester.error("Error insert failed");

    if nodes[0].nextSibling != None:
        tester.error("Error insert failed");
    if nodes[0].previousSibling.nodeName != nodes[1].nodeName:
        tester.error("Error insert failed");
    if nodes[1].nextSibling.nodeName != nodes[0].nodeName:
        tester.error("Error insert failed");
    if nodes[1].previousSibling != None:
        tester.error("Error insert failed");

    if p.removeChild(nodes[1]).nodeName != nodes[1].nodeName:
        tester.error("Error Removing")
    if p.firstChild.nodeName != nodes[0].nodeName:
        tester.error("Error Remove Failed")
    if p.lastChild.nodeName != nodes[0].nodeName:
        tester.error("Error RemoveFailed")
    if nodes[1].nextSibling != None:
        tester.error("Error Remove Failed");
    if nodes[1].previousSibling != None:
        tester.error("Error Remove Failed");
    if nodes[0].nextSibling != None:
        tester.error("Error Remove Failed");
    if nodes[0].previousSibling != None:
        tester.error("Error Remove Failed");

    try:
        p.insertBefore(nodes[2],nodes[1]);
    except DOMException, x:
        if x.code != NOT_FOUND_ERR:
            name = get_exception_name(x.code)
            tester.error("Wrong exception '%s', expected NOT_FOUND_ERR" % name)
    tester.testDone()


    tester.startTest("Testing replaceChild")
    if p.replaceChild(nodes[1], nodes[0]).nodeName != nodes[0].nodeName:
        tester.error("ReplaceChild Does not work")

    if p.firstChild.nodeName != nodes[1].nodeName:
        tester.error("ReplaceChild Does not work")
    if p.lastChild.nodeName != nodes[1].nodeName:
        tester.error("ReplaceChild Does not work")

    if nodes[1].nextSibling != None:
        tester.error("ReplaceChild Does not work")
    if nodes[1].previousSibling != None:
        tester.error("ReplaceChild Does not work")

    if nodes[0].nextSibling != None:
        tester.error("ReplaceChild Does not work")
    if nodes[0].previousSibling != None:
        tester.error("ReplaceChild Does not work")
    try:
        p.replaceChild(nodes[0],nodes[0] )
    except DOMException, x:
        if x.code != NOT_FOUND_ERR:
            name = get_exception_name(x.code)
            tester.error("Wrong exception '%s', expected NOT_FOUND_ERR" % name)
    tester.testDone()


    tester.startTest("Testing removeChild")
    try:
        p.removeChild(nodes[0]);
    except DOMException, x:
        if x.code != NOT_FOUND_ERR:
            name = get_exception_name(x.code)
            tester.error("Wrong exception '%s', expected NOT_FOUND_ERR" % name)
    if p.removeChild(nodes[1]).nodeName != nodes[1].nodeName:
        tester.error("Error Remove Failed");

    if p.firstChild != None:
        tester.error("Error Remove Failed");
    if p.lastChild != None:
        tester.error("Error Remove Failed");
    if nodes[1].nextSibling != None:
        tester.error("Error Remove Fialed");
    if nodes[1].previousSibling != None:
        tester.error("Error Remove Failed");
    tester.testDone()


    tester.startTest("Testing appendChild()")
    if p.appendChild(nodes[0]).nodeName != nodes[0].nodeName:
        tester.error("Error Append Failed");
    if nodes[0].parentNode.nodeName != p.nodeName:
        tester.error('AppendChild faild to set parent');
    if p.firstChild.nodeName != nodes[0].nodeName:
        tester.error("Error Append Failed");
    if p.lastChild.nodeName != nodes[0].nodeName:
        tester.error("Error Append Failed");
    if nodes[0].nextSibling!= None:
        tester.error("Error Append Failed");
    if nodes[0].previousSibling != None:
        tester.error("Error Append Failed")
    tester.testDone()


    tester.startTest("Testing hasChildNodes()")
    if not p.hasChildNodes():
        tester.error("Error hasChildNodes");
    p.removeChild(nodes[0]);
    if p.hasChildNodes():
        tester.error("Error hasChildNodes")
    tester.testDone()


    tester.startTest("Testing supports()")
    if nodes[1].supports('XML','') != 1:
        tester.error("Supports failed")
    tester.testDone()


    tester.startTest('Testing normalize()')
    e = doc.createElement('TEST');
    e1 = doc.createElement('TAG3')

    t1 = doc.createTextNode('String1');
    t2 = doc.createTextNode(' String2');
    t3 = doc.createTextNode(' String 3');
    t4 = doc.createTextNode(' String 4');
    e.appendChild(t1);
    e.appendChild(t2);
    e.appendChild(t3);
    e.appendChild(e1);
    e.appendChild(t4);

    e.normalize();
    if e.childNodes.length != 3:
        tester.error('Normalize did not work');
    tester.testDone()


    tester.startTest("Testing cloneNode() [single]")
    p1 = e.cloneNode(0)
    if p1.nodeName != e.nodeName:
        tester.error("cloneNode failed on nodeName")
    if p1.nodeValue != e.nodeValue:
        tester.error("cloneNode failed on nodeValue")
    if p1.nodeType != e.nodeType:
        tester.error("cloneNode failed on nodeType")
    if p1.ownerDocument.nodeName != e.ownerDocument.nodeName:
        tester.error("cloneNode failed on ownerDocument")
    tester.testDone()


    tester.startTest("Testing cloneNode() [deep]")
    p2 = e.cloneNode(1)
    #Verify the same number of different children
    if p2.childNodes.length != e.childNodes.length:
        tester.error("cloneNode didn\'t copy all of the nodes");
    if p2.firstChild == e.firstChild:
        tester.error("cloneNode failed on firstChild")
    if p2.lastChild == e.lastChild:
        tester.error("cloneNode failed on lastChild")
    if p2.childNodes.item(1) == e.childNodes.item(1):
        tester.error("cloneNode has the same children");
    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys

    import TestSuite
    tester = TestSuite.TestSuite(1, 1)

    retVal = test(tester)
    sys.exit(retVal)
