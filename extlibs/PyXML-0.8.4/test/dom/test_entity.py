from TestSuite import EMPTY_NAMESPACE
def test(tester):

    tester.startGroup('Entity')

    tester.startTest('Testing syntax')
    try:
        from xml.dom import Entity
        from xml.dom.Entity import Entity
    except:
        tester.error('Error in syntax', 1)
    tester.testDone()


    tester.startTest('Creating test environment')
    from xml.dom import implementation
    dt = implementation.createDocumentType('','','')
    doc = implementation.createDocument(EMPTY_NAMESPACE,'ROOT',dt)

    ent = doc._4dom_createEntity("-//FOURTHOUGHT//EN", "/tmp/entity", "")
    tester.testDone()


    tester.startTest('Testing attributes')
    if ent.publicId != '-//FOURTHOUGHT//EN':
        tester.error('publicId is incorrect')
    if ent.systemId != '/tmp/entity':
        tester.error('systemId is incorrect')
    tester.testDone()


    tester.startTest('Test cloneNode()')
    ent1 = ent.cloneNode(1)
    if ent1.publicId != ent.publicId:
        tester.error("cloneNode fails on publicId")

    if ent1.systemId != ent.systemId:
        tester.error("cloneNode fails on systemId")
    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
