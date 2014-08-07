from TestSuite import EMPTY_NAMESPACE
def printer(tester, tw, spc):
    n = tw.currentNode
    tester.message("%s<%s>" % (spc, n.nodeName))
    child = tw.firstChild()
    while child:
        printer(tester, tw, spc + '  ')
        child = tw.nextSibling()
        if not child:
            tw.parentNode()
    tester.message("%s</%s>" % (spc, n.nodeName))

def test(tester):

    tester.startGroup('TreeWalker')

    tester.startTest('Checking syntax')
    from xml.dom.TreeWalker import TreeWalker
    tester.testDone()

    tester.startTest('Creating test environment')
    from xml.dom import implementation
    from xml.dom.NodeFilter import NodeFilter
    from xml.dom.ext.reader import Sax

    dt = implementation.createDocumentType('','','')
    doc = implementation.createDocument(EMPTY_NAMESPACE,None,dt);

    xml_string = '<a><b><c/><d/></b><e><f/><g/></e></a>'
    doc = Sax.FromXml(xml_string)
    from xml.dom.ext import PrettyPrint
    tw = TreeWalker(doc.documentElement, NodeFilter.SHOW_ELEMENT, None, 1)
    tester.testDone()


    tester.startTest('Testing attributes')
    if tw.root != doc.documentElement:
        tester.error('root was not set')
    if tw.whatToShow != NodeFilter.SHOW_ELEMENT:
        tester.error('whatToShow was not set')
    if tw.filter != None:
        tester.error('filter was not set')
    if tw.expandEntityReferences != 1:
        tester.error('expandEntityReferences was not set')
    tw.currentNode = doc.documentElement.lastChild
    if tw.currentNode != doc.documentElement.lastChild:
        tester.error('currentNode does not set/get properly')
    tester.testDone()


    tester.startTest("Navigating in document order")
    tw.currentNode = tw.root
    if tw.currentNode.nodeName != 'a':
        tester.error('currentNode failed')
    t = doc.createTextNode('Text')
#    tw.currentNode.insertBefore(t,tw.firstChild())
    if tw.firstChild().nodeName != 'b':
        tester.error('Wrong firstChild')
    if tw.nextSibling().nodeName != 'e':
        tester.error('Wrong nextSibling')
    if tw.nextSibling() != None:
        tester.error('nextSibling returns a value; should be (null)')
    if tw.parentNode().nodeName != 'a':
        tester.error('Wrong parentNode')
    if tw.lastChild().nodeName != 'e':
        tester.error('Wrong lastChild')
    if tw.nextNode().nodeName != 'f':
        tester.error('Wrong nextNode')
    # See if whatToShow works
    tw.currentNode.appendChild(t)
    if tw.firstChild() != None:
        tester.error('whatToShow failed in firstChild()')
    if tw.previousSibling() != None:
        tester.error('previousSibling returns a value; should be (null)')
    if tw.previousNode().nodeName != 'e':
        tester.error('Wrong previousNode')
    tw.currentNode.appendChild(t)
    # See if whatToShow works
    if tw.lastChild().nodeName != 'g':
        tester.error('whatToShow failed in lastChlid()')
    tester.testDone()


#    tester.startTest('Printing hierarchy')
#    xml.dom.ext.PrettyPrint(tw.root)
#    tw.currentNode = tw.root
#    printer(tester, tw, '')
#    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys

    import TestSuite
    tester = TestSuite.TestSuite(0,1)

    retVal = test(tester)
    sys.exit(retVal)
