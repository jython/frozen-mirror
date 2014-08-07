# A DOM benchmark

import sys, time

from xml.dom import core, utils

def main():
    global L, doc
    if len(sys.argv) == 1:
        print 'Usage: benchmark.py <xml file>'
        sys.exit()

    filename = sys.argv[1]

    file = open(filename, 'r')
    size = len(file.read())
    file.close()

    print 'File %s is %iK in size' % (filename, size / 1024)

    start_time = time.time()
    doc = utils.FileReader( filename ).document
    end_time = time.time()
    print 'Building DOM tree:', end_time - start_time, 'sec'

    # Convert DOM tree back to XML
    start_time = time.time()
    xml = doc.toxml()
    end_time = time.time()
    print 'Serializing back to XML:', end_time - start_time, 'sec'

    # Time a complete getElementsByTagName()
    start_time = time.time()
    L = doc.getElementsByTagName("*")
    end_time = time.time()
    print 'getElementsByTagName("*"):', end_time - start_time, 'sec'
    print L[0].nodeName

if __name__ == '__main__': main()
