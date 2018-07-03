"""
Test raising a tuple.
"""

import support

error = "anerror"

try:
    raise (error,), "value"
except error:
    pass
except BaseException:
    raise support.TestError('Should have been caught by except clause')
