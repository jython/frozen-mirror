from TestSuite import EMPTY_NAMESPACE
def get_exception_name(code):
    import types
    from xml import dom
    for (name,value) in vars(dom).items():
        if (type(value) == types.IntType
        and value == code):
            return name

def test(tester):

    tester.startGroup('NamedNodeMap')

    tester.startTest('Checking syntax')
    try:
        from xml.dom import NamedNodeMap
        from xml.dom.NamedNodeMap import NamedNodeMap
    except:
        tester.error('Error in syntax', 1)
    tester.testDone()


    tester.startTest("Creating test environment")
    nodes = []
    from xml.dom import implementation
    dt = implementation.createDocumentType('','','')
    doc = implementation.createDocument(EMPTY_NAMESPACE,'ROOT',dt)

    try:
        for ctr in range(3):
            n = doc.createElement('Node%d'%(ctr+1))
            nodes.append(n)
    except:
        tester.error("Unable to create test nodes")
    nm = doc.createElement('TEST').attributes
    tester.testDone()


    tester.startTest("Testing setNamedItem()")
    if nm.setNamedItem(nodes[0]) != None:
        tester.error("setNamedItem failed")
    if nm.length != 1:
        tester.error("setNamedItem failed")

    nodes[2] = doc.createElement('Node1')

    if nm.setNamedItem(nodes[2]).nodeName != nodes[0].nodeName:
        tester.error("setNamedItem failed on replace")
    if nm.length != 1:
        tester.error("setNamedItem failed")
    tester.testDone()


    tester.startTest("Testing getNamedItem()")
    if nm.getNamedItem(nodes[2].nodeName).nodeName != nodes[2].nodeName:
        tester.error("getNamedItem returns wrong Node")
    if nm.getNamedItem(nodes[1].nodeName) != None:
        tester.error("getNamedItem returns a Node instead of null")
    tester.testDone()


    tester.startTest("Testing removeNamedItem()")
    nodes[0] = doc.createElement("NewNode1")
    nm.setNamedItem(nodes[0]);

    if nm.length != 2:
        tester.error("setNamedItem failed")

    if nm.removeNamedItem(nodes[0].nodeName).nodeName != nodes[0].nodeName:
        tester.error("removeNamedItem failed")

    if nm.length != 1:
        tester.error("removeNamedItem failed")

    from xml.dom import DOMException
    from xml.dom import NOT_FOUND_ERR
    try:
        nm.removeNamedItem(nodes[0].nodeName)
    except DOMException, err:
        if err.code != NOT_FOUND_ERR:
            name = get_exception_name(x.code)
            tester.error("Wrong exception '%s', expected NOT_FOUND_ERR" % name)

    if nm.length != 1:
        tester.error("removeNamedItem failed")
    tester.testDone()


    tester.startTest("Testing item()")
    if nm.item(0).nodeName != nodes[2].nodeName:
        tester.error("item failed")
    if nm.item(1) != None:
        tester.error("item failed")
    tester.testDone()


    tester.startTest("Testing setNamedItemNS()")
    node = doc.createElementNS('www.fourthought.com', 'ft:Node4')
    if nm.setNamedItemNS(node) != None:
        tester.error('setNamedItemNS returns a value; should be (null)')
    tester.testDone()


    tester.startTest("Testing getNamedItemNS()")
    if nm.getNamedItemNS('www.fourthought.com', 'Node4').nodeName != node.nodeName:
        tester.error("getNamedItemNS failed")
    tester.testDone()


    tester.startTest("Testing removeNamedItemNS()")
    if nm.removeNamedItemNS('www.fourthought.com', 'Node4').nodeName != node.nodeName:
        tester.error("removeNamedItemNS failed")
    if nm.length != 1:
        tester.error("removeNamedItemNS failed")
    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':

    import sys
    import TestSuite

    testSuite = TestSuite.TestSuite()
    retVal = test(testSuite)
    sys.exit(retVal)
