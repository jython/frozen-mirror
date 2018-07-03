
import sys
import atexit


def myfunc():
    print "myfunc"


atexit.register(myfunc)
