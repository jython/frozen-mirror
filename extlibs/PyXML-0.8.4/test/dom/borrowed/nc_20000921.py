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


source_1 = """<xsltemplate match="email/headers[substring-after(subject,'address')]"/>"""


expected_1 = """\
<?xml version='1.0' encoding='UTF-8'?><!DOCTYPE xsltemplate><xsltemplate match="email/headers[substring-after(subject,\'address\')]"/>"""


def Test(tester):

    tester.startGroup("Nicolas Chauvat <nico@logilab.com>'s Printer Bug Report")

    tester.startTest('Attribute quote print')
    d=Sax2.FromXml(source_1)
    stream = cStringIO.StringIO()
    Print(d, stream=stream)
    result = stream.getvalue()
    if result != expected_1:
        tester.error('Expected\n"""%s"""\ngot\n"""%s"""'%(repr(expected_1), repr(result)))

    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = Test(tester)
    sys.exit(retVal)
