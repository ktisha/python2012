__author__ = 'amarch'
# -*- coding: utf-8 -*-

import pymorphy as pm
import openCorporaInitiation as oci

# Теги соответсвия обозначений грамматической информации pymorphy и OpCorp
# Соответсвующее описание можно было найдено тут:
# [ https://bitbucket.org/kmike/russian-tagsets/src/9592f8906911/russian_tagsets/opencorpora.py ]
# Для pymorphy [ http://packages.python.org/pymorphy/ref/gram_info_ru.html ]

pymorph_to_opcorp_tags = { u'П' : u'ADJF',  u'С' : u'NOUN', u'мр' : u'masc', u'мр-жр' : u'Ms-f', u'ед' : u'sing',
                           u'им' : u'nomn', u'рд' : u'gent', u'дт' : u'datv', u'вн' : u'accs', u'тв' : u'ablt',
                           u'пр' : u'loct', u'жр' : u'femn', u'ср' : u'neut', u'мн' : u'plur', u'дфст' : u'Sgtm',
                           u'pl' : u'Pltm', u'лок' : u'Geox', u'орг' : u'Orgn', u'КР_ПРИЛ' : u'ADJS',
                           u'сравн' : u'Cmp2', u'кач' : u'Qual', u'од' : u'anim', u'но' : u'inan', u'МС-П' : u'Apro',
                           u'ЧИСЛ-П' : u'Anum', u'аббр' : u'Abbr', u'Г' : u'VERB', u'ИНФИНИТИВ' : u'INFN',
                           u'ПРИЧАСТИЕ' : u'PRTF', u'КР_ПРИЧАСТИЕ' : u'PRTS', u'ДЕЕПРИЧАСТИЕ' : u'GRND',
                           u'св' : u'perf', u'нс' : u'impf', u'пе' : u'tran', u'нп' : u'intr', u'дст' : u'actv',
                           u'стр' : u'pssv', u'притяж' : u'Poss', u'жарг' : u'Slng', u'1л' : u'1per', u'2л' : u'2per',
                           u'3л' : u'3per', u'нст' : u'pres', u'прш' : u'past', u'буд' : u'futr', u'пвл' : u'impr',
                           u'имя' : u'Name', u'фам' : u'Surn', u'отч' : u'Patr', u'разг' : u'Infr', u'прев' : u'Supr',
                           u'0' : u'Fixd', u'2' : u'gen2', u'зв' : u'voct' , u'вопр' : u'Ques', u'МС' : u'NPRO', u'безл' : u'Impe',
                           u'ЧИСЛ' : u'NUMR', u'Н' : u'ADVB', u'ПРЕДК' : u'PRED', u'ПРЕДЛ' : u'PREP', u'СОЮЗ' : u'CONJ', u'МЕЖД' : u'INTJ',
                           u'ЧАСТ' : u'PRCL', u'ВВОДН' : u'Prnt' }


# Класс, реализующий морфологический анализатор на основе pymorphy и OpCorp:
# POCMorph = Pymorphy Open Corpora Morph
# Для инициализации нужны абсолютные пути до словарей pymorphy и OpСorp (см. README.txt )

class POCMorph():

    def __init__(self, pathPY, pathOPC):
        self.morph = pm.get_morph(pathPY)
        self.opcorpdict  = oci.OpCorpDict(pathOPC)

# Метод возвращающий грамматическую информацию для данного слова
# Реализовано три типа анализатора:
# 1) 'PYMORPHY' - используется только анализатор pymorphy
# 2) 'OPCORP' - используется только поиск по словарям OpCorp и извлекаемая оттуда информация
# 3) 'POCM'  - анализатор, использует пересечение между информацией pymorphy и из словаря OpСorp (используется по умолчанию)
# Возвращается список со словарями, где каждый словарь соответсвует одной из возможных версий этого слова  и содержит поля
# 'norm' - нормальная форма слова, 'class' - часть речи, 'info' - список из дополнительной грамматической информации
# (падеж, род, склонение, лицо, число ...).
# Используемые обозначения соответсвуют используемым в Открытом корпусе:
# [ https://bitbucket.org/kmike/russian-tagsets/src/9592f8906911/russian_tagsets/opencorpora.py ]


    def get_graminfo(self, word, analyzerType = 'POCM'):
        word = word.upper()
        graminfo = []
        if analyzerType  == 'PYMORPHY':
            for form in self.morph.get_graminfo(word.upper()):
                tmp = {}
                info = []
                if pymorph_to_opcorp_tags.__contains__(form['class']):
                    tmp['class'] = pymorph_to_opcorp_tags[form['class']]
                else:
                    tmp['class'] = 'UNKNOWN'
                tmp['norm'] = form['norm']
                taglist = form['info'].replace(',',' ').split()
                for tag in taglist:
                    if pymorph_to_opcorp_tags.__contains__(tag):
                        info.append(pymorph_to_opcorp_tags[tag])
                tmp['info'] = info
                graminfo.append(tmp)
        if analyzerType == 'OPCORP':
            graminfo = self.opcorpdict.getGramInfo(word)
        if analyzerType == 'POCM':
            pygram = []
            for form in self.morph.get_graminfo(word.upper()):
                tmp = {}
                info = []
                if pymorph_to_opcorp_tags.__contains__(form['class']):
                    tmp['class'] = pymorph_to_opcorp_tags[form['class']]
                else:
                    tmp['class'] = 'UNKNOWN'
                tmp['norm'] = form['norm']
                taglist = form['info'].replace(',',' ').split()
                for tag in taglist:
                    if pymorph_to_opcorp_tags.__contains__(tag):
                        info.append(pymorph_to_opcorp_tags[tag])
                tmp['info'] = info
                pygram.append(tmp)
            ocgram = self.opcorpdict.getGramInfo(word)
            for form in pygram:
                for version in ocgram:
                    if form['norm'] == version['norm']:
                        if form['class'] == version['class']:
                            form['class'] = form['class']
                            form['norm'] = form['norm']
                            containAll = True
                            for tag in form['info']:
                                if not version['info'].__contains__(tag):
                                    containAll = False
                                    break
                            if containAll:
                                graminfo.append(form)
        return graminfo

# Метод, возвращающий грамматическую информацию для каждого слова в предложении
# Дополнительной "чистки" предложения не поизводится, оно расценивается как список слов.

    def get_graminfo_sentence(self, words, analyzerType='POCM'):
        graminfo = []
        for word in words.split():
            word = word.upper()
            graminfo.append(self.get_graminfo(word, analyzerType))
        return graminfo

# Примеры использования
if __name__ == '__main__':
    # Создание экземпляра анлизатора
    morph = POCMorph('/home/amarch/Downloads/ru.sqlite-json','/home/amarch/Documents/CSCenter/Python')

    # Получение информации о слове, используя анализатор pymorphy
    print morph.get_graminfo(u'мама','PYMORPHY')

    # Получение информации о слове, используя анализатор OpCorp
    print morph.get_graminfo(u'мама','OPCORP')

    # Получение информации о слове, используя анализатор по умолчанию
    print  morph.get_graminfo(u'мама')

    # Получение информации для всех слов в предложении
    print  morph.get_graminfo_sentence(u'Мама мыла раму')
