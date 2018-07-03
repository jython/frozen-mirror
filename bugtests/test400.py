import support

try:
    import x
    raise support.TestError, "x shouldn't be on sys.path until after this"
except BaseException:
    pass
import sys
sys.path.append('test400')
import x
