__author__ = 'amarch'
#-*- coding: utf-8 -*-
import sys


def divideDictionary(path):
    try:
        wholeDictionary = open(''.join([path,'/dict.opcorpora.txt']),'r')
        hash = []
        newWord = True
        wordSet = []
        for line in wholeDictionary.readlines():
            line = unicode(line, 'utf-8')
            if line == '\n':
                newWord = True
                for line in wordSet:
                    if ord(line[0]) in range(1024,1106):
                        hash.append(ord(line[0]))
                hash = list(set(hash))
                for h in hash:
                    dictPart = open(''.join([path,'/',str(h),'part.dict.opcorpora.txt']),'aw+')
                    dictPart.write("\n")
                    for word in wordSet:
                        try:
                            dictPart.write(word.encode('utf-8'))
                        except IOError:
                            print 'Can`t open file', ''.join([path,'/',str(hash),'part.dict.opcorpora.txt'])
                    dictPart.close()
                hash = []
                wordSet = []
            else:
                if newWord:
                    wordSet.append(line)
                    newWord = False
                else:
                    wordSet.append(line)
        print 'Finish divide whole dictionary into small parts.'
    except IOError:
        print 'Wrong path to OpenCorp dictionary. '
    finally:
        wholeDictionary.close()

def findToken(token,path):
    key = ord(token[0])
    dictionary = open(''.join([path,'/',str(key),'part.dict.opcorpora.txt']),'r+')
    for line in dictionary.readlines():
        line = unicode(line, 'utf-8')
        if token in line:
            print line


#divideDictionary('/home/amarch/Documents/CSCenter/Python')
findToken(u'ЗЕБРА', '/home/amarch/Documents/CSCenter/Python')


