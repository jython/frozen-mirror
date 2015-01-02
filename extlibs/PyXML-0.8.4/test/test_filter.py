import pprint
import sys

from xml.dom import xmlbuilder, expatbuilder, Node
from xml.dom.NodeFilter import NodeFilter

class Filter(xmlbuilder.DOMBuilderFilter):
    whatToShow = NodeFilter.SHOW_ELEMENT

    def startContainer(self, node):
        assert node.nodeType == Node.ELEMENT_NODE
        if node.tagName == "skipthis":
            return self.FILTER_SKIP
        elif node.tagName == "rejectbefore":
            return self.FILTER_REJECT
        elif node.tagName == "stopbefore":
            return self.FILTER_INTERRUPT
        else:
            return self.FILTER_ACCEPT

    def acceptNode(self, node):
        assert node.nodeType == Node.ELEMENT_NODE
        if node.tagName == "skipafter":
            return self.FILTER_SKIP
        elif node.tagName == "rejectafter":
            return self.FILTER_REJECT
        elif node.tagName == "stopafter":
            return self.FILTER_INTERRUPT
        else:
            return self.FILTER_ACCEPT


class RecordingFilter:
    # Inheriting from xml.dom.xmlbuilder.DOMBuilderFilter is not
    # required, so we won't inherit from it this time to make sure it
    # isn't a problem.  We have to implement the entire interface
    # directly.

    whatToShow = NodeFilter.SHOW_ALL

    def __init__(self):
        self.events = []

    def startContainer(self, node):
        self.events.append(("start", node.nodeType, str(node.nodeName)))
        return xmlbuilder.DOMBuilderFilter.FILTER_ACCEPT

    def acceptNode(self, node):
        self.events.append(("accept", node.nodeType, str(node.nodeName)))
        return xmlbuilder.DOMBuilderFilter.FILTER_ACCEPT


simple_options = xmlbuilder.Options()
simple_options.filter = Filter()
simple_options.namespaces = 0

record_options = xmlbuilder.Options()
record_options.namespaces = 0

def checkResult(src):
    print
    dom = expatbuilder.makeBuilder(simple_options).parseString(src)
    print dom.toxml()
    dom.unlink()

def checkFilterEvents(src, record, what=NodeFilter.SHOW_ALL):
    record_options.filter = RecordingFilter()
    record_options.filter.whatToShow = what
    dom = expatbuilder.makeBuilder(record_options).parseString(src)
    if record != record_options.filter.events:
        print
        print "Received filter events:"
        pprint.pprint(record_options.filter.events)
        print
        print "Expected filter events:"
        pprint.pprint(record)
    dom.unlink()


# a simple case of skipping an element
checkResult("<doc><e><skipthis>text<e/>more</skipthis>abc</e>xyz</doc>")

# skip an element nested indirectly within another skipped element
checkResult('''\
<doc>Text.
  <skipthis>Nested text.
    <skipthis>Nested text in skipthis element.</skipthis>
    More nested text.
  </skipthis>Outer text.</doc>
''')

# skip an element nested indirectly within another skipped element
checkResult('''\
<doc>Text.
  <skipthis>Nested text.
    <nested-element>
      <skipthis>Nested text in skipthis element.</skipthis>
      More nested text.
    </nested-element>
    More text.
  </skipthis>Outer text.</doc>
''')

checkResult("<doc><rejectbefore/></doc>")

checkResult("<doc><rejectafter/></doc>")

checkResult('''\
<doc><rejectbefore>
  Text.
  <?my processing instruction?>
  <more stuff="foo"/>
  <!-- a comment -->
</rejectbefore></doc>
''')

checkResult('''\
<doc><rejectafter>
  Text.
  <?my processing instruction?>
  <more stuff="foo"/>
  <!-- a comment -->
</rejectafter></doc>
''')

# Make sure the document element is not passed to the filter:
checkResult("<rejectbefore/>")
checkResult("<rejectafter/>")
checkResult("<stopbefore/>")

checkResult("<doc>text<stopbefore> and </stopbefore>more</doc>")
checkResult("<doc>text<stopafter> and </stopafter>more</doc>")

checkResult("<doc><a/><skipafter>text</skipafter><a/></doc>")

checkFilterEvents("<doc/>", [])
checkFilterEvents("<doc attr='value'/>", [])
checkFilterEvents("<doc><e/></doc>", [
    ("start", Node.ELEMENT_NODE, "e"),
    ("accept", Node.ELEMENT_NODE, "e"),
    ])

src = """\
<!DOCTYPE doc [
  <!ENTITY e 'foo'>
  <!NOTATION n SYSTEM 'http://xml.python.org/notation/n'>
]>
<!-- comment -->
<?sample pi?>
<doc><e attr='value'><?pi data?><!--comment--></e></doc>
"""

checkFilterEvents(src, [
    ("accept", Node.DOCUMENT_TYPE_NODE, "doc"),
    ("accept", Node.ENTITY_NODE, "e"),
    ("accept", Node.NOTATION_NODE, "n"),
    ("accept", Node.COMMENT_NODE, "#comment"),
    ("accept", Node.PROCESSING_INSTRUCTION_NODE, "sample"),
    ("start", Node.ELEMENT_NODE, "e"),
    ("accept", Node.PROCESSING_INSTRUCTION_NODE, "pi"),
    ("accept", Node.COMMENT_NODE, "#comment"),
    ("accept", Node.ELEMENT_NODE, "e"),
    ])

# Show everything except a couple of things to the filter, to check
# that whatToShow is implemented.  This isn't sufficient to be a
# black-box test, but will get us started.

checkFilterEvents(src, [
    ("accept", Node.DOCUMENT_TYPE_NODE, "doc"),
    ("accept", Node.ENTITY_NODE, "e"),
    ("accept", Node.NOTATION_NODE, "n"),
    ("accept", Node.PROCESSING_INSTRUCTION_NODE, "sample"),
    ("start", Node.ELEMENT_NODE, "e"),
    ("accept", Node.PROCESSING_INSTRUCTION_NODE, "pi"),
    ("accept", Node.ELEMENT_NODE, "e"),
    ], what=NodeFilter.SHOW_ALL & ~NodeFilter.SHOW_COMMENT)

checkFilterEvents(src, [
    ("accept", Node.DOCUMENT_TYPE_NODE, "doc"),
    ("accept", Node.ENTITY_NODE, "e"),
    ("accept", Node.NOTATION_NODE, "n"),
    ("accept", Node.COMMENT_NODE, "#comment"),
    ("start", Node.ELEMENT_NODE, "e"),
    ("accept", Node.COMMENT_NODE, "#comment"),
    ("accept", Node.ELEMENT_NODE, "e"),
    ], what=NodeFilter.SHOW_ALL & ~NodeFilter.SHOW_PROCESSING_INSTRUCTION)
