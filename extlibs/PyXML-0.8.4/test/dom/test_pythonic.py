#!/usr/bin/env python

from TestSuite import EMPTY_NAMESPACE

def test(tester):
    tester.startGroup('Python Representation')

    tester.startTest('Creating test environment')
    from xml.dom import implementation
    dt = implementation.createDocumentType('','','')
    doc = implementation.createDocument(EMPTY_NAMESPACE,'ROOT',dt)
    c = doc.createComment("Comment")
    tester.testDone()


    tester.startTest('Test Attribute')
    a = doc.createAttribute('ATTR_NAME')
    a.value = 'ATTR_VALUE'
    tester.message(str(a))
    tester.testDone()


    tester.startTest('Testing CDATASection')
    c1 = doc.createCDATASection('Short String')
    tester.message(str(c1))
    c2 = doc.createCDATASection('This is a much longer string, over 20 characters')
    tester.message(str(c2))
    tester.testDone()


    tester.startTest('Testing Comment')
    c1 = doc.createComment('Short Comment')
    tester.message(str(c1))
    c2 = doc.createComment('This is a much longer comment, over 20 characters')
    tester.message(str(c2))
    tester.testDone()


    tester.startTest('Testing Document')
    tester.message(str(doc))
    tester.testDone()


    tester.startTest('Testing Document Fragment')
    df = doc.createDocumentFragment()
    tester.message(str(df))
    tester.testDone()


    tester.startTest('Testing Element')
    e = doc.createElement('ELEMENT')
    tester.message(str(e))
    tester.testDone()


    tester.startTest('Testing Entity')
    e = doc._4dom_createEntity("ID1","ID2","NAME")
    tester.message(str(e))
    tester.testDone()


    tester.startTest('Testing Entity Reference')
    e = doc.createEntityReference('E-Ref')
    tester.message(str(e))
    tester.testDone()


    tester.startTest('Testing NamedNodeMap')
    nnm = implementation._4dom_createNamedNodeMap()
    tester.message(str(nnm))
    tester.testDone()


    tester.startTest('Testing NodeList')
    nl = implementation._4dom_createNodeList([e])
    tester.message(str(nl))
    tester.testDone()


    tester.startTest('Testing Notation')
    n = doc._4dom_createNotation("ID1","ID2","NAME")
    tester.message(str(n))
    tester.testDone()


    tester.startTest('Testing ProcessingInstruction')
    p = doc.createProcessingInstruction('This-is-a-long-target', 'short data')
    tester.message(str(p))
    tester.testDone()


    tester.startTest('Testing Text')
    t = doc.createTextNode('This is a very long text string')
    tester.message(str(t))
    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
