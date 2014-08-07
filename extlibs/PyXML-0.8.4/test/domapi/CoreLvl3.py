"""Test cases for DOM Core Level 3."""

import xml.dom

import Base


class WhitespaceInElementContentTestCase(Base.TestCaseBase):

    def checkWhiteSpaceInElementContent(self):
        TEXT = """<!DOCTYPE doc [
          <!ELEMENT doc (foo+)>
        ]>
        <doc>
          <foo/>
        </doc>"""
        doc = self.parse(TEXT)
        for node in doc.documentElement.childNodes:
            if node.nodeType == xml.dom.Node.TEXT_NODE:
                if not node.isWhitespaceInElementContent:
                    self.fail("founc whitespace node not identified"
                              " as whitespace-in-element-contnet")

    def checkWhiteSpaceInUnknownContent(self, subset=""):
        TEXT = """<!DOCTYPE doc %s>
        <doc>
          <foo/>
        </doc>""" % subset
        doc = self.parse(TEXT)
        for node in doc.documentElement.childNodes:
            if node.nodeType == xml.dom.Node.TEXT_NODE:
                if node.isWhitespaceInElementContent:
                    self.fail("founc whitespace node in mixed content marked"
                              " as whitespace-in-element-contnet")

    def _checkWhiteSpaceInMixedContent(self):
        # XXX this test is confused
        self.checkWhiteSpaceInUnknownContent("""[
          <!ELEMENT doc (#PCDATA | foo)*>
        ]""")


cases = Base.buildCases(__name__, 'Core', '3.0')
