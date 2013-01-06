import getopt
import sys
from task import Task

__author__ = 'Aleksandr Vereshchagin'

def usage():
    print 'Usage:'
    print 'python main.py <action> -o|--output outputFile inputFile'
    print '    action is one of:'
    print '-c, --compress: compress bmp image'
    print '-x, --extract: extract bmp image'
    print ''
    print 'Example:'
    print 'python main.py -c -o data/dest.cim data/image.bmp'

def processArgs(optlist, inputs, task):
    if len(inputs) > 0:
        task.withInput(inputs[0])
    for opt, arg in optlist:
        if opt in ('-c', '--compress'):
            task.withAction('compress')
        elif opt in ('-x', '--extract'):
            task.withAction('extract')
        elif opt in ('-o', '--output'):
            task.withOutput(arg)
        else:
            print 'Unsupported option'

def main():
    task = Task()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'cxo:',
            ['compress', 'extract', 'output='])
        processArgs(optlist, args, task)
    except getopt.GetoptError as e:
        print str(e)
        usage()
        return
    task.run()

if __name__ == '__main__':
    main()
