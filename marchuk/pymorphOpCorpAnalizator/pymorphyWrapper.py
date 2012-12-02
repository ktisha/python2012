__author__ = 'amarch'
#-*- coding: utf-8 -*-
import sys
import pymorphy as pm
import openCorporaInitiation as oci
import sys


class POCMorph():

    def __init__(self, path):
        self.morph = pm.get_morph(path)

    def get_graminfo_sentence(self, words):
        graminfo = []
        for word in words.split():
            #word = word.encode('utf-8')
            word = word.upper()
            graminfo.append(self.morph.get_graminfo(word,standard=True))
        return graminfo

    def get_graminfo(self,word,standard=True):
        return self.morph.get_graminfo(word,standard=True)


if __name__ == '__main__':
    opcordict = oci.OpCorpDict('/home/amarch/Documents/CSCenter/Python')
    morph = POCMorph('/home/amarch/Downloads/ru.sqlite-json')
    info = morph.get_graminfo(u'ДЕЛАЮ', standard=True)
    print info
    print morph.get_graminfo_sentence(u'Мама мыла раму')