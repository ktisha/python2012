__author__ = 'amarch'
# -*- coding: utf-8 -*-
from openCorporaInitiation import *
from opcorpTextProcessing import *
from pymorphyWrapper import *
import time

start_time = time.time()

sentences =  getSentences_fromXML("/home/amarch/Documents/CSCenter/Python/corpus/annot.opcorpora.no_ambig.xml",10)
morph = POCMorph('/home/amarch/Downloads/ru.sqlite-json','/home/amarch/Documents/CSCenter/Python')

finish_sent_time = time.time()

#for s in sentences:
#    print s

pymorphy_points = 0
pocmorph_points = 0
opc_points = 0
pytime = 0
poctime = 0
opctime = 0


for sent in sentences:
    for tokens in sent[1:]:
        for token in tokens:
            word = token[0]
            pytime -= time.time()
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
            pytime += time.time()

            poctime -= time.time()
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
            poctime += time.time()

            opctime -= time.time()
            opc_list = morph.get_graminfo(word,'OPCORP')
            for form in opc_list:
                if form['norm'] == token[1]['norm'].upper():
                    if form['class'] == token[1]['class']:
                        infoset = True
                        for tag in form['info']:
                            if not token[1]['info'].__contains__(tag):
                                infoset = False
                                break
                        if infoset:
                            opc_points += 1.0/len(opc_list)
            opctime += time.time()


print 'Pymorphy score:  ', pymorphy_points, ' time ',  pytime
print 'POCMorph score:  ', pocmorph_points, ' time ', poctime
print 'OpCorp score:  ', opc_points, ' time ', opctime

print 'Time: for proceed',len(sentences),' sentences ', finish_sent_time - start_time, "seconds"
print 'Total time: ', time.time() - start_time
