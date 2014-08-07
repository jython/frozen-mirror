from TestSuite import EMPTY_NAMESPACE
from xml.dom import DOMException
from xml.dom import NO_MODIFICATION_ALLOWED_ERR

def get_exception_name(code):
    import types
    from xml import dom
    for (name,value) in vars(dom).items():
        if (type(value) == types.IntType
        and value == code):
            return name

def test(tester):

    tester.startGroup('NodeList')

    tester.startTest('Checking syntax')
    try:
        from xml.dom import NodeList
        from xml.dom.NodeList import NodeList
    except:
        tester.error('Error in syntax',1)
    tester.testDone()


    tester.startTest('Creating the test environment')
    try:
        from xml.dom import implementation
        dt = implementation.createDocumentType('','','')
        doc = implementation.createDocument(EMPTY_NAMESPACE,'ROOT',dt)
    except:
        tester.error('Error creating document')

    nodes = []
    try:
        for ctr in range(3):
            nodes.append(doc.createElement('Node%d' %ctr))
    except:
        tester.error("Error creating nodes")

    e = doc.createElement('PARENT')
    try:
        for n in nodes:
            e.appendChild(n)
    except:
        tester.error('Error appending nodes')
    nl = e.childNodes
    tester.testDone()


    tester.startTest("Testing attributes")
    if nl.length != 3:
        tester.error('length reports wrong amount')
    try:
        nl.length = 5
    except DOMException, x:
        if x.code != NO_MODIFICATION_ALLOWED_ERR:
            name = get_exception_name(x.code)
            tester.error("Wrong exception '%s', expected NOMODIFICATION_ALLOWED_ERR" % name)
    else:
        tester.error('length not read-only')
    tester.testDone()


    tester.startTest("Testing item()")
    if nl.item(0).nodeName != nodes[0].nodeName:
        tester.error("Item returns wrong item")
    if nl.item(3) != None:
        tester.error("Item returns something on invalid index")
    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
