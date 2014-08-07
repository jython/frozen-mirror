# This demo converts a few nested objects into an XML representation,
# and provides a simple example of using the Builder class.

from xml.dom import core
from xml.dom.builder import Builder

import types, time

def object_convert(builder, obj):

    # Put the entire object inside an element with the same name as
    # the class.
    builder.startElement( obj.__class__.__name__ )
    L = obj.__dict__.keys()
    L.sort()

    for attr in obj.__dict__.keys():

        # Skip internal attributes (ones that begin with a '_')
        if attr[0] == '_': continue

        value = getattr(obj, attr)
        if type(value) == types.InstanceType:
            # Recursively process subobjects
            object_convert( builder, value)

        else:
            # Convert anything else to a string and put it in an element
            builder.startElement(attr)
            builder.text( str(value) )
            builder.endElement(attr)

    builder.endElement( obj.__class__.__name__ )

if __name__ == '__main__':
    class Folder: pass
    class Bookmark: pass

    f=Folder()
    f.title = "Folder Title"
    f.createdTime = time.asctime( time.localtime( time.time() ) )
    f.bookmark = b = Bookmark()
    b.url, b.title = "http://www.python.org", "Python Home Page"

    builder = Builder()
    object_convert(builder, f)
    print "Output from two nested objects:"
    print builder.document.toxml()
