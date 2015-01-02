from TestSuite import EMPTY_NAMESPACE
def test(tester):

    tester.startGroup('NodeIterator')


    tester.startTest('Checking syntax')
    try:
        from xml.dom import NodeIterator
        from xml.dom.NodeIterator import NodeIterator
    except:
        tester.error('Error in syntax', 1)
    tester.testDone()

    tester.startTest('Creating test environment')
    from xml.dom import implementation
    doc = implementation.createDocument(EMPTY_NAMESPACE,None,None);

    #xml_string = '<a><b><c/><d/></b><e><f/><g/></e></a>'
    try:
        a = doc.createElement('a')
        b = doc.createElement('b')
        c = doc.createElement('c')
        d = doc.createElement('d')
        e = doc.createElement('e')
        f = doc.createElement('f')
        g = doc.createElement('g')
    except:
        tester.error('Couldn\'t create elements')
    try:
        b.appendChild(c)
        b.appendChild(d)
        a.appendChild(b)
        e.appendChild(f)
        e.appendChild(g)
        a.appendChild(e)
        doc.appendChild(a)
    except:
        tester.error('Counl\'t append to DOM tree')

    from xml.dom.NodeFilter import NodeFilter
    nit = doc.createNodeIterator(doc, NodeFilter.SHOW_ELEMENT, None,1)
    tester.testDone()


    tester.startTest('Iterating forward')
    curr_node =  nit.nextNode()
    while curr_node:
        curr_node =  nit.nextNode()
    tester.testDone()


    tester.startTest('Iterating in reverse')
    curr_node =  nit.previousNode()
    while curr_node:
        curr_node =  nit.previousNode()
    tester.testDone()


    tester.startTest('Iterating forward again')
    curr_node =  nit.nextNode()
    while curr_node:
        curr_node =  nit.nextNode()
    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
