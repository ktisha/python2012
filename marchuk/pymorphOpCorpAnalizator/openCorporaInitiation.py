__author__ = 'amarch'
#-*- coding: utf-8 -*-
import sys


def divideDictionary(path):
    try:
        wholeDictionary = open(''.join([path,'/dict.opcorpora.txt']),'r')
        hash = 1025
        dictPart = open(''.join([path,'/',str(hash),'part.dict.opcorpora.txt']),'aw+')
        newWord = True
        for line in wholeDictionary.readlines():
            line = unicode(line, 'utf-8')
            if not (ord(line[0]) in range(1024,1106)):
                newWord = True
                dictPart.write(line.encode('utf-8'))
            else:
                if newWord:
                    if ord(line[0]) != hash:
                        try:
                            dictPart.close()
                        except IOError:
                            print 'Can`t close', dictPart.name
                        hash = ord(line[0])
                        try:
                            dictPart = open(''.join([path,'/',str(hash),'part.dict.opcorpora.txt']),'aw+')
                            #print 'Create file', ''.join([path,'/',str(hash),'part.dict.opcorpora.txt'])
                            dictPart.write(line.encode('utf-8'))
                        except IOError:
                            print 'Can`t create file', ''.join([path,'/',str(hash),'part.dict.opcorpora.txt'])
                    newWord = False
                else:
                    dictPart.write(line.encode('utf-8'))
    except IOError:
        print 'Wrong path to OpenCorp dictionary. '
    finally:
        wholeDictionary.close()


divideDictionary('/home/amarch/Documents/CSCenter/Python')


