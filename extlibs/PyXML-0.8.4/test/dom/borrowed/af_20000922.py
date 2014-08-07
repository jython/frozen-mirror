import cStringIO
from xml.dom import DOMException
from xml.dom import NAMESPACE_ERR
from xml.dom.ext import Print, PrettyPrint
from xml.dom.ext.reader import Sax2

def GetExceptionName(code):
    import types
    from xml import dom
    for (name,value) in vars(dom).items():
        if (type(value) == types.IntType and value == code):
            return name

source_1 = """<?xml version='1.0' encoding='iso-8859-1'?>
<element>àéèêëïîöôùü</element>"""


expected_1 = """\
<?xml version='1.0' encoding='UTF-8'?><!DOCTYPE element><element>\303\240\303\251\303\250\303\252\303\253\303\257\303\256\303\266\303\264\303\271\303\274</element>"""


expected_2 = """\
<?xml version='1.0' encoding='UTF-8'?><!DOCTYPE element><element>àéèêëïîöôùü</element>"""


def Test(tester):

    tester.startGroup("Alexander Fayolle's encoding problems and variations")

    tester.startTest('XML output UTF-8 encoding')
    d=Sax2.FromXml(source_1)
    stream = cStringIO.StringIO()
    Print(d, stream=stream)
    result = stream.getvalue()
    if result != expected_1:
        tester.error('Expected\n"""%s"""\ngot\n"""%s"""'%(repr(expected_1), repr(result)))
    tester.testDone()

    tester.startTest('XML output ISO-8859-1 encoding')
    d=Sax2.FromXml(source_1)
    stream = cStringIO.StringIO()
    Print(d, stream=stream, encoding='ISO-8859-1')
    result = stream.getvalue()
    if result != expected_2:
        tester.error('Expected\n"""%s"""\ngot\n"""%s"""'%(repr(expected_2), repr(result)))
    tester.testDone()

    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = Test(tester)
    sys.exit(retVal)
