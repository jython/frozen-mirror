source_1 = """<ot:message xmlns:ot='http://namespaces.opentechnology.org/talk' xmlns:doc='http://docbook.org/docbook/xml/4.0/namespace' ot:id='urn:90f00-20e-d03-406-2020f01903'>
  <dc:subject xmlns:dc='http://purl.org/metadata/dublin_core'>XML Blaster</dc:subject>
  <dc:title xmlns:dc='http://purl.org/metadata/dublin_core'>Re: Blaster</dc:title>
  <dc:content xmlns:dc='http://purl.org/metadata/dublin_core'>
<doc:emph>Bitchin</doc:emph>
  <ot:signature><BR class='hack'/><HR class='hack'/>By Test Super User</ot:signature></dc:content>
<ot:reply-to ot:id='urn:f050b05-108-e00-805-f0f0c037'/><dc:creator xmlns:dc = 'http://purl.org/metadata/dublin_core' ot:id='urn:1020d0d-f0c-a06-f0f-2020b07a01' ot:name='Super Test User'/><dc:datetime xmlns:dc='http://purl.org/metadata/dublin_core'>2000-08-19 13:56:42-0600</dc:datetime></ot:message>"""


def test(tester):
    tester.startGroup('XML With Namespaces')

    tester.startTest('Namespaces multiply defined at 2nd level')
    from xml.dom.ext.reader import Sax2
    import xml.dom.ext
    doc = Sax2.FromXml(source_1)
    xml.dom.ext.Print(doc)
    tester.testDone()

    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
