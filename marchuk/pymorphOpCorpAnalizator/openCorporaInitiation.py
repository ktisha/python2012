__author__ = 'amarch'
# -*- coding: utf-8 -*-

import os


# Класс, релализующий работу со словарем Открытого корпуса русского языка [opencorpora.org]

class OpCorpDict():

    path = ''

# Метод инициализации словаря, аргументами служат путь до словаря и флаг принудительного разбиения.
# Для ускорения работы со словарем, имеющем не менее 5 миллионов вхождений, словарь разбивается на отдельные части
# вида Xpart.dict.opcorpora.txt, где X - числовой код первой буквы слова.
# Разбиение происходит один раз, все части сохраняются в папку '/divideOpCorp', возможно принудительное разбиение
# при установленном флаге 'divide=True'.

    def __init__(self, path, divide=False):
        self.path = path
        if divide:
            try:
                os.removedirs(''.join([path, '/dividedOpCorp']))
                os.makedirs(''.join([path, '/dividedOpCorp']))
                self.divideDictionary()
            except IOError,OSError:
                print 'OpCorpDict can\'t divide dictionary. Please check your rights in destination. '
        else:
            if not os.path.exists(''.join([path, '/dividedOpCorp'])):
                os.makedirs(''.join([path, '/dividedOpCorp']))
                self.divideDictionary()
        self.path = ''.join([path, '/dividedOpCorp'])

# Метод разбиения словаря
# Разбиение происходит по первой букве слова, если у слова есть формы на разные буквы (ЕХАТЬ и ПОЕХАТЬ) - все формы
# записываются во все подходящие файлы

    def divideDictionary(self):
        print 'Start divide whole dictionary into small parts. Please wait.'
        try:
            wholeDictionary = open(''.join([self.path,'/dict.opcorpora.txt']),'r')
            letterHashes = []
            newWord = True
            wordSet = []
            for line in wholeDictionary.readlines():
                line = unicode(line, 'utf-8')
                if line == '\n':
                    newWord = True
                    for line in wordSet:
                        if ord(line[0]) in range(1024,1106):
                            letterHashes.append(ord(line[0]))
                    letterHashes = list(set(letterHashes))
                    for h in letterHashes:
                        dictPart = open(''.join([self.path,'/dividedOpCorp/',str(h),'part.dict.opcorpora.txt']),'aw+')
                        dictPart.write("\n")
                        for word in wordSet:
                            try:
                                dictPart.write(word.encode('utf-8'))
                            except IOError:
                                print 'Can`t open file', ''.join([self.path,'/dividedOpCorp/',str(letterHashes),'part.dict.opcorpora.txt'])
                        dictPart.close()
                    letterHashes = []
                    wordSet = []
                else:
                    if newWord:
                        wordSet.append(line)
                        newWord = False
                    else:
                        wordSet.append(line)
            wholeDictionary.close()
            print 'Finish divide whole dictionary into small parts.'
        except IOError:
            print 'Wrong path to OpenCorp dictionary, cant open dictionary file. '

# Метод, выводящий все возможные совпадения слов в словаре со словами из входного предложения

    def findWord(self, sentence):
        matches = []
        for token in sentence.split():
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

# Метод, возвращающий всю найденную в словаре для данного слова грамматическую информацию
# Для каждого найденного вхождения возвращается словарь с ключами 'norm' - нормальная форма слова, 'class' - часть речи,
# 'info' - список остальной информации (падеж, часть речи, лицо, склонение...). Описание обозначений смотреть тут:
#  [ https://bitbucket.org/kmike/russian-tagsets/src/9592f8906911/russian_tagsets/opencorpora.py ]

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

# Метод, вовзвращающий все возможные формы слова, найденные в словаре.
# С помощью этого метода можно например склонять глаголы по падежам.
# Возвращается список, где каждое вхождение - пара из формы слова и информации по ней

    def getAllForms(self, word):
        word = word.upper()
        key = ord(word[0])
        forms = []
        tmp = []
        newEntity = False
        try:
            dictionary = open(''.join([self.path,'/',str(key),'part.dict.opcorpora.txt']),'r+')
        except IOError:
            return []
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

# Примеры использования
if __name__ == '__main__':

    # Создание экземпляра словаря
    opcordict = OpCorpDict('/home/amarch/Documents/CSCenter/Python')

    # Все вхождения для слов из предложения
    opcordict.findWord(u'Мама мыла раму')

    # Все вхождения слова в словарь
    opcordict.findWord(u'делаю')

    # Все формы данного слова
    all = opcordict.getAllForms(u'делаю')
    for form in all:
        print 'New form of u\'делаю\':\n'
        for ind in form:
            print ind['form'],ind['info']

    # Информация из словаря для данного слова
    print opcordict.getGramInfo(u'делаю')
