# built-in tests
from xml.marshal import generic, wddx

generic.runtests()
wddx.runtests()

# additional tests
try:
    from test.test_support import verify
except ImportError:
    from test.test_support import TestFailed
    def verify(condition, reason="test failed"):
        if not condition:
            raise TestFailed(reason)

# test for correct processing of ignorable whitespace
data = """<?xml version="1.0"?>
<marshal>
  <list id="i2">
    <int>1</int>
    <int>2</int>
  </list>
</marshal>"""

verify(generic.loads(data) == [1, 2])
