import cStringIO
from xml.dom import DOMException
from xml.dom.ext import Print
from xml.dom.ext.reader import PyExpat, Sax2


def GetExceptionName(code):
    import types
    from xml import dom
    for (name,value) in vars(dom).items():
        if (type(value) == types.IntType and value == code):
            return name


expected_1 = source_1 = """\
<?xml version="1.0" encoding='utf-8'?>
<memo id="mydoc" xmlns:mkt="http://our.industry.org/schema/product-info"
      xmlns="http://xml-typographers.org/typo-markup-standard/1.0">
  <category>Marketing Request</category>
  <!-- A test comment -->
  <title>Re: Widget 404 Request</title>
  <para>
    <?PI test pi?>
    We need 5 of
      <mkt:product code="00808">
        <mkt:name>Widget 404</mkt:name>
        <mkt:description><![CDATA[Gee-gaw &]]> doo-dad</mkt:description>
      </mkt:product>
    to send out to reviewers this week.
  </para>
</memo>"""


expected_2 = source_2 = """\
<outer xmlns="">
  <inner xmlns="http://www.ietf.org"/>
</outer>
"""


#expected_1 = """<xsltemplate match="email/headers[substring-after(subject,\'address\')]"/>"""


def Test(tester):

    tester.startGroup("Testing PyExpat")

    reader = PyExpat.Reader()

    tester.startTest('Basic test')
    doc = reader.fromString(source_1)
    stream = cStringIO.StringIO()
    Print(doc, stream=stream)
    result = stream.getvalue()
    print result
    #if result != expected_1:
    #    tester.error('Expected\n"""%s"""\ngot\n"""%s"""'%(repr(expected_1), repr(result)))

    reader.releaseNode(doc)

    tester.groupDone()


    tester.startGroup("Testing Sax2")

    reader = Sax2.Reader()

    tester.startTest('Basic test')
    doc = reader.fromString(source_1)
    stream = cStringIO.StringIO()
    Print(doc, stream=stream)
    result = stream.getvalue()
    print result
    #if result != expected_1:
    #    tester.error('Expected\n"""%s"""\ngot\n"""%s"""'%(repr(expected_1), repr(result)))

    reader.releaseNode(doc)

    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = Test(tester)
    sys.exit(retVal)
