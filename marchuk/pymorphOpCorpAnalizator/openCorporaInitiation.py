__author__ = 'amarch'
# -*- coding: utf-8 -*-
import sys
import os




class OpCorpDict():

    path = ''

    def __init__(self, path, divide=False):
        self.path = path
        if divide:
            try:
                os.removedirs(''.join([path, '/dividedOpCorp']))
                os.makedirs(''.join([path, '/dividedOpCorp']))
                self.divideDictionary()
            except Exception:
                print 'Good news everyone!'
        else:
            if not os.path.exists(''.join([path, '/dividedOpCorp'])):
                os.makedirs(''.join([path, '/dividedOpCorp']))
                self.divideDictionary()
        self.path = ''.join([path, '/dividedOpCorp'])

    def divideDictionary(self):
        print 'Start divide whole dictionary into small parts. Please wait.'
        try:
            wholeDictionary = open(''.join([self.path,'/dict.opcorpora.txt']),'r')
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
                        dictPart = open(''.join([self.path,'/dividedOpCorp/',str(h),'part.dict.opcorpora.txt']),'aw+')
                        dictPart.write("\n")
                        for word in wordSet:
                            try:
                                dictPart.write(word.encode('utf-8'))
                            except IOError:
                                print 'Can`t open file', ''.join([self.path,'/dividedOpCorp/',str(hash),'part.dict.opcorpora.txt'])
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

    def findWord(self, words):
        matches = []
        for token in words.split():
            token = token.upper()
            key = ord(token[0])
            dictionary = open(''.join([self.path,'/',str(key),'part.dict.opcorpora.txt']),'r+')
            print '\nFounded next words, related to', token, ' in  OpCorp:\n',
            for line in dictionary.readlines():
                line = unicode(line, 'utf-8')
                if ''.join([token,'	']) in line[0:len(token)+1]:
                    print line[:-2]
                    matches.append(line[:-2])
            if matches == []:
                print 'Nothing >:(\n'

    def getGramInfo(self, word):
            word = word.upper()
            forms = self.getAllForms(word)
            graminfo = []
            for version in forms:
                tmp = {}
                tmp['norm'] = version[0]['form']
                for entity in version:
                    if entity['form'] == word:
                        splited = entity['info'].replace(',',' ').split()
                        tmp['class'] = splited[0]
                        tmp['info'] = splited[1:]
                graminfo.append(tmp)
            return graminfo

    def getAllForms(self, word):
        word = word.upper()
        key = ord(word[0])
        forms = []
        tmp = []
        newEntity = False
        dictionary = open(''.join([self.path,'/',str(key),'part.dict.opcorpora.txt']),'r+')
        for line in dictionary.readlines():
            line = unicode(line, 'utf-8')
            if line == '\n':
                if newEntity:
                    forms.append(tmp)
                newEntity = False
                tmp = []
            else:
                if not line[:-2].isdigit():
                    tmp.append({  'form':line.split()[0], 'info':line[(line.split()[0].__len__()):]  })
            if ''.join([word,'	']) in line[0:len(word)+1]:
                newEntity = True
        return forms


if __name__ == '__main__':
    #Examples
    opcordict = OpCorpDict('/home/amarch/Documents/CSCenter/Python')
    #opcordict.findWord(u'Мама мыла раму')
#    opcordict.findWord(u'делаю')
    all = opcordict.getAllForms(u'делаю')
    for form in all:
        print 'New form:\n'
        for ind in form:
            print ind['form'], ind['info']
#    print opcordict.getGramInfo(u'делаю')
#    all =  opcordict.getAllForms(u'злословия')
#    print all
#    for ent in all:
#        for x in ent:
#            print x['form']
    # ITS A TRAP!
#    opcordict.findWord(u'Выходить')
