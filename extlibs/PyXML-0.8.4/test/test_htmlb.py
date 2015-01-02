# dom.html_builder tests

from xml.dom.ext.reader import HtmlLib
from xml.dom.ext import XHtmlPrettyPrint
import sys

good_html = """
<html>
<body>
<P>I prefer (all things being equal) regularity/orthogonality and logical
syntax/semantics in a language because there is less to have to remember.
(Of course I <em>know</em> all things are NEVER really equal!)
<P CLASS=source>Guido van Rossum, 6 Dec 91
<P>The details of that silly code are irrelevant.
<P CLASS=source>Tim Peters, 4 Mar 92
&amp; &lt; &gt; &eacute; &ouml; &nbsp;
</body>
</html>
"""

bad_html = """
<html>
Interdigitated <b>bold and <i>italic</B> tags.</i>&amp; &lt; &gt; &eacute; &ouml; &nbsp;
</html>
"""

# Try the good output with both settings of ignore_mismatched_end_tags
# At the moment, don't; HtmlLib does not have these two modes of
# operation.

print "Good document"
b = HtmlLib.FromHtml(good_html)
#b.expand_entities = b.expand_entities + ('eacute',)
XHtmlPrettyPrint(b, stream=sys.stdout, encoding = "ISO-8859-1")

# Sgmlop currently does not complain about mismatched or misplaced tags
# or other aspects of invalidity.
#  print "Bad document"
#  try:
#      HtmlLib.FromHtml(bad_html)
#  except html_builder.BadHTMLError:
#      print "Exception raised for bad HTML"
#  else:
#      print "*** ERROR: no exception raised for bad HTML"
