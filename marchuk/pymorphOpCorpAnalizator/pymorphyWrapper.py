__author__ = 'amarch'
# -*- coding: utf-8 -*-
import sys
import pymorphy as pm
import openCorporaInitiation as oci
import sys


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


class POCMorph():

    def __init__(self, path):
        self.morph = pm.get_morph(path)

    def get_graminfo_sentence(self, words):
        graminfo = []
        for word in words.split():
            #word = word.encode('utf-8')
            word = word.upper()
            graminfo.append(self.morph.get_graminfo(word))
        return graminfo

    def get_graminfo(self,word):
        return self.morph.get_graminfo(word)


if __name__ == '__main__':
    opcordict = oci.OpCorpDict('/home/amarch/Documents/CSCenter/Python')
    morph = POCMorph('/home/amarch/Downloads/ru.sqlite-json')
    info = morph.get_graminfo(u'ДЕЛАЮ')
    print info
    print info[0]['info']
    print morph.get_graminfo_sentence(u'Мама мыла раму')