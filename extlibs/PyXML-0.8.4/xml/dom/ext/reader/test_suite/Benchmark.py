from xml.dom.ext.reader import Sax2

def Benchmark(fileName):

    return Sax2.FromXmlFile(fileName)




if __name__ == '__main__':

    import time,sys
    sTime = time.time()
    d = Benchmark(sys.argv[1])
    print "Total Time: %f" % (time.time() - sTime)


    from xml.dom import ext
    ext.Print(d)
