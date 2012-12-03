__author__ = 'amarch'
# -*- coding: utf-8 -*-
from openCorporaInitiation import *
from opcorpTextProcessing import *
from pymorphyWrapper import *
import time


sentences =  getSentences_fromXML("/home/amarch/Documents/CSCenter/Python/corpus/annot.opcorpora.no_ambig.xml")
morph = POCMorph('/home/amarch/Downloads/ru.sqlite-json','/home/amarch/Documents/CSCenter/Python')

#for s in sentences:
#    print s

pymorphy_points = 0
pocmorph_points = 0

start_time = time.time()

for sent in sentences:
    for tokens in sent[1:]:
        for token in tokens:
            word = token[0]
            pym_list = morph.get_graminfo(word,'PYMORPHY')
            for form in pym_list:
                if form['norm'] == token[1]['norm'].upper():
                    if form['class'] == token[1]['class']:
                        infoset = True
                        for tag in form['info']:
                            if not token[1]['info'].__contains__(tag):
                                infoset = False
                                break
                        if infoset:
                            pymorphy_points += 1.0/len(pym_list)
            pocm_list = morph.get_graminfo(word)
            for form in pocm_list:
                if form['norm'] == token[1]['norm'].upper():
                    if form['class'] == token[1]['class']:
                        infoset = True
                        for tag in form['info']:
                            if not token[1]['info'].__contains__(tag):
                                infoset = False
                                break
                        if infoset:
                            pocmorph_points += 1.0/len(pocm_list)

print 'Pymorphy score:  ', pymorphy_points
print 'POCMorph score:  ', pocmorph_points
print 'Time: for ',len(sentences),' sentences ', time.time() - start_time, "seconds"
