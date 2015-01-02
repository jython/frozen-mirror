from TestSuite import EMPTY_NAMESPACE
def test(tester):
    tester.startGroup('DOMImplementation')

    tester.startTest('Checking syntax')
    try:
        from xml.dom import DOMImplementation
        from xml.dom.DOMImplementation import DOMImplementation
    except:
        tester.error('Error in syntax', 1)
    tester.testDone()


    tester.startTest('Creating test environment')
    from xml.dom import implementation
    di = implementation
    tester.testDone()


    tester.startTest('Testing hasFeature()')
    if di.hasFeature('XML', '2.0') == 0:
        tester.error('hasFeature does not get feature with version');
    if di.hasFeature('XML', '') == 0:
        tester.error('hasFeature does not get feature (any version)');
    tester.testDone()


    tester.startTest('Testing createDocumentType()')
    dt = di.createDocumentType('NAME','PUBLICID','SYSTEMID')
    if dt.nodeName != 'NAME':
        tester.error('createDocumnent does not set qualifiedName properly')
    if dt.publicId != 'PUBLICID':
        tester.error('createDocumnent does not set namespaceURI properly')
    if dt.systemId != 'SYSTEMID':
        tester.error('createDocumnent does not set doctype properly')
    tester.testDone()


    tester.startTest('Testing createDocument()')
    doc = di.createDocument(EMPTY_NAMESPACE,'NAME',dt)
    if doc.namespaceURI != None:
        tester.error('createDocumnent does not set namespaceURI properly')
    if doc.documentElement.nodeName != 'NAME':
        tester.error('createDocumnent does not set qualifiedName properly')
    if doc.doctype != dt:
        tester.error('createDocumnent does not set doctype properly')
    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
