__author__ = 'amarch'
#-*- coding: utf-8 -*-
import sys
import pymorphy as pm
import openCorporaInitiation as oci

def get_graminfo_sentence(words, morph):
    graminfo = []
    for word in words:
        word = unicode(word,'utf-8')
        word = word.upper()
        graminfo.append(morph.get_graminfo(word))
    return graminfo


if __name__ == '__main__':
    opcordict = oci.OpCorpDict('/home/amarch/Documents/CSCenter/Python')
    morph = pm.get_morph('/home/amarch/Downloads/ru.sqlite-json')
    info = morph.get_graminfo(u'ДЕЛАЮ',standard=True)
    print info