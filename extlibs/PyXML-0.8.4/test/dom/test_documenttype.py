def test(tester):

    tester.startGroup('DocumentType')

    tester.startTest('Testing syntax')
    try:
        from xml.dom import DocumentType
        from xml.dom.DocumentType import DocumentType
    except:
        tester.tester.error('Error in syntax', 1)
    tester.testDone()


    tester.startTest('Creating test environment')
    from xml.dom import implementation
    dt = implementation.createDocumentType('TEST','PublicID','SystemID')
    tester.testDone()


    tester.startTest('Testing attributes')
    if dt.name != 'TEST':
        tester.error('name is incorrect')
    if dt.publicId != 'PublicID':
        tester.error('publicId is incorrect')
    if dt.systemId != 'SystemID':
        tester.error('systemId is incorrect')
    tester.testDone()


    tester.startTest('Testing cloneNode()')
    #Should always be done deep
    dt1 = dt.cloneNode(1)
    if dt1.name != dt.name:
        tester.error("cloneNode failed on name")
    if dt1.entities.length != dt.entities.length:
        tester.error("cloneNode did not copy all entities")
    if dt1.notations.length != dt.notations.length:
        tester.error("cloneNode did not copy all notations")
    if dt1.publicId != dt.publicId:
        tester.error("cloneNode fails on publicId")
    if dt1.systemId != dt.systemId:
        tester.error("cloneNode fails on systemId")
    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
