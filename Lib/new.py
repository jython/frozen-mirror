"""Create new objects of various types.  Deprecated.

This module is no longer required except for backward compatibility.
Objects of most types can now be created by calling the type object.
"""
from warnings import warnpy3k
warnpy3k("The 'new' module has been removed in Python 3.0; use the 'types' "
         "module instead.", stacklevel=2)
del warnpy3k


# XXX: Jython can't really create a code object like CPython does
# (according to test.test_new)
from org.python.core import PyBytecode as code
