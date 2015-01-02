from TestSuite import EMPTY_NAMESPACE
from xml.dom import DOMException
from xml.dom import HIERARCHY_REQUEST_ERR
from xml.dom import WRONG_DOCUMENT_ERR
from xml.dom import NOT_FOUND_ERR

from Ft.Lib import TestSuite

class NodeTestCase(TestSuite.TestCase):
    def create(self):
        from xml.dom import implementation
        dt = implementation.createDocumentType('','','')
        doc = implementation.createDocument(EMPTY_NAMESPACE,'ROOT',dt)

        #We cannot use just plain old nodes, we need to use Elements
        self.pNode = doc.createElement('PARENT')

        self.nodes = []
        for ctr in range(3):
            n = doc.createElement('Child %d' % ctr)
            self.nodes.append(n);

    def testSyntax(self):
        from xml.dom import Node
        from xml.dom.Node import Node

    def testNodeName(self):
        if self.pNode.nodeName != 'PARENT':
            raise TestSuiteError('error getting nodeName')

    def testNodeValue(self):
        self.pNode.nodeValue = 'NODE_VALUE'
        if self.pNode.nodeValue != 'NODE_VALUE':
            raise TestSuiteError('error with get/set nodeVaLue')

    def testNodeType(self):
        if self.pNode.nodeType != Node.ELEMENT_NODE:
            raise TestSuiteError('error getting nodeType')

    def test(FIXME):





        test = group.newTest("Testing attributes")
        if p.nodeName != 'PARENT':
            test.error("Error getting NodeName");
        p.nodeValue = 'NodeValue';
        if p.nodeValue != 'NodeValue':
            test.error('Error getting/setting NodeValue');
        if p.nodeType != Node.ELEMENT_NODE:
            test.error('Error getting NodeType');
        if p.parentNode != None:
            test.error('Error getting parentNode');
        p._4dom_setParentNode(None)
        if p.firstChild != None:
            test.error('Error getting FirstChild');
        if p.lastChild != None:
            test.error('Error getting Last Child');
        if p.nextSibling != None:
            test.error('Error getting Next Sibling');
        if p.previousSibling != None:
            test.error('Error getting Previous Sibling');
        if p.attributes == None:
            test.error('Error getting attributes');
        if p.ownerDocument.nodeName != doc.nodeName:
            test.error('Error getting ownerDocument');
        if p.namespaceURI != '':
            test.error('Error namespaceURI')
        if p.prefix != '':
            test.error('Error Prefix')
        if p.localName != p.nodeName:
            test.error('Error localName')


        group.newTest("Testing insertBefore()")
        if p.insertBefore(nodes[0],None).nodeName != nodes[0].nodeName:
            test.error("Error inserting");

        if p.firstChild.nodeName != nodes[0].nodeName:
            test.error("Error insert failed");
        if p.lastChild.nodeName != nodes[0].nodeName:
            test.error("Error insert failed");

        if p.insertBefore(nodes[1],nodes[0]).nodeName != nodes[1].nodeName:
            test.error("Error inserting");

        if p.firstChild.nodeName != nodes[1].nodeName:
            test.error("Error insert failed");
        if p.lastChild.nodeName != nodes[0].nodeName:
            test.error("Error insert failed");

        if nodes[0].nextSibling != None:
            test.error("Error insert failed");
        if nodes[0].previousSibling.nodeName != nodes[1].nodeName:
            test.error("Error insert failed");
        if nodes[1].nextSibling.nodeName != nodes[0].nodeName:
            test.error("Error insert failed");
        if nodes[1].previousSibling != None:
            test.error("Error insert failed");

        if p.removeChild(nodes[1]).nodeName != nodes[1].nodeName:
            test.error("Error Removing")
        if p.firstChild.nodeName != nodes[0].nodeName:
            test.error("Error Remove Failed")
        if p.lastChild.nodeName != nodes[0].nodeName:
            test.error("Error RemoveFailed")

        if nodes[1].nextSibling != None:
            test.error("Error Remove Failed");
        if nodes[1].previousSibling != None:
            test.error("Error Remove Failed");
        if nodes[0].nextSibling != None:
            test.error("Error Remove Failed");
        if nodes[0].previousSibling != None:
            test.error("Error Remove Failed");

        try:
            p.insertBefore(nodes[2],nodes[1]);
        except DOMException, e:
            if e.code != NOT_FOUND_ERR:
                raise e


        group.newTest("Testing replaceChild")
        if p.replaceChild(nodes[1], nodes[0]).nodeName != nodes[0].nodeName:
            test.error("ReplaceChild Does not work")

        if p.firstChild.nodeName != nodes[1].nodeName:
            test.error("ReplaceChild Does not work")
        if p.lastChild.nodeName != nodes[1].nodeName:
            test.error("ReplaceChild Does not work")

        if nodes[1].nextSibling != None:
            test.error("ReplaceChild Does not work")
        if nodes[1].previousSibling != None:
            test.error("ReplaceChild Does not work")

        if nodes[0].nextSibling != None:
            test.error("ReplaceChild Does not work")
        if nodes[0].previousSibling != None:
            test.error("ReplaceChild Does not work")

        try:
            p.replaceChild(nodes[0],nodes[0] )
        except DOMException, e:
            if e.code != NOT_FOUND_ERR:
                raise e;


        group.newTest("Testing removeChild")
        try:
            p.removeChild(nodes[0]);
        except DOMException, e:
            if e.code != NOT_FOUND_ERR:
                raise e

        if p.removeChild(nodes[1]).nodeName != nodes[1].nodeName:
            test.error("Error Remove Failed");

        if p.firstChild != None:
            test.error("Error Remove Failed");
        if p.lastChild != None:
            test.error("Error Remove Failed");
        if nodes[1].nextSibling != None:
            test.error("Error Remove Fialed");
        if nodes[1].previousSibling != None:
            test.error("Error Remove Failed");


        group.newTest("Testing appendChild")
        if p.appendChild(nodes[0]).nodeName != nodes[0].nodeName:
            test.error("Error Append Failed");

        if nodes[0].parentNode.nodeName != p.nodeName:
            test.error('AppendChild faild to set parent');
        if p.firstChild.nodeName != nodes[0].nodeName:
            test.error("Error Append Failed");
        if p.lastChild.nodeName != nodes[0].nodeName:
            test.error("Error Append Failed");
        if nodes[0].nextSibling!= None:
            test.error("Error Append Failed");
        if nodes[0].previousSibling != None:
            test.error("Error Append Failed")


        group.newTest("Testing hasChildNodes")
        if not p.hasChildNodes():
            test.error("Error hasChildNodes");
        p.removeChild(nodes[0]);
        if p.hasChildNodes():
            test.error("Error hasChildNodes")


        group.newTest("Testing supports")
        if nodes[1].supports('XML','') != 1:
            test.error("Supports failed")


        group.newTest('Testing normalize()')
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
            test.error('Normalize did not work');


        group.newTest("Testing cloneNode")
        p.appendChild(nodes[0])

        #Shallow copy
        '''p1 = Node.cloneNode(p,0);

        if p1.nodeName != p.nodeName:
                test.error("CloneNode Failed Node Name");
        if p1.nodeValue != p.nodeValue:
                test.error("CloneNode Failed Node Value")
        if p1._get_nodeType() != p._get_nodeType():
                test.error("CloneNode Failed Node Type")
        if p1.ownerDocument.nodeName != p.ownerDocument.nodeName:
                test.error("CloneNode Failed Owner Document")
        if p1.firstChild == p.firstChild:
                test.error("CloneNode Failed FirstChild")
        if p1.lastChild == p.lastChild:
                test.error("CloneNode Failed LastChild")

        print "Shallow Copy works"


        #Deep copy
        p2 = Node.cloneNode(p,1);
        #Verify the same number of different children
        if p2.getChildNodes().getLength() != p.getChildNodes().getLength():
                test.error("CloneNode Failed");

        if p2.getChildNodes().item(0) == p.getChildNodes().item(0):
                test.error("CloneNode Failed");

        print "Deep Copy works"'''

        return 1


if __name__ == '__main__':

    from Ft.Lib import TestSuite
    testSuite = TestSuite.TestSuite(4, None, 0, 1)

    test(testSuite)
