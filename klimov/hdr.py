import sys
from main import *

def print_help():
    print "This is programm to hand written digits recognition."
    print "To scan Images just pass filenames to argv."
    print "\nExample: \"python hdr.py test1.jpg\"\n"
    print "Notice, that digits recognize in left-right prientation."
    print "You will need this package: scipy, numpy, PIL."


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'ERROR: type filename to scan'
        sys.exit()

    if sys.argv[1] == '--help' or sys.argv[1] == '-h':
        print_help()
        sys.exit(0) 


    for i in range(len(sys.argv) - 1):  
        print 'Image %d - %s'% (i+1, str(scan_image(sys.argv[i+1])))
