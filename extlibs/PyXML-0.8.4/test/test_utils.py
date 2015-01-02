# Test the modules in the utils/ subpackage
# FIXME: escape is now in xml.sax.saxutils, need to move testcase as well

from xml.utils import *
from xml.sax.saxutils import escape

print 'Testing utils.escape'
print 'These pairs of strings should all be identical'

v1, v2 = escape('&<>'), '&amp;&lt;&gt;'
print int(v1 == v2), repr(v1), repr(v2)
v1, v2 = escape('foo&amp;bar'), 'foo&amp;amp;bar'
print int(v1 == v2), repr(v1), repr(v2)
v1, v2 = escape('< test > &', {'test': '&myentity;'}), '&lt; &myentity; &gt; &amp;'
print int(v1 == v2), repr(v1), repr(v2)
v1, v2 = escape('&\'"<>', {'"': '&quot;', "'": '&apos;'}), '&amp;&apos;&quot;&lt;&gt;'
print int(v1 == v2), repr(v1), repr(v2)

# Test the iso8601 module

for dt in ['1998', '1998-06', '1998-06-13',
           '1998-06-13T14:12Z',
           '1998-06-13T14:12:30Z',
           '1998-06-13T14:12:30.2Z'
           ]:
    date = iso8601.parse( dt )
    print iso8601.tostring( date )
