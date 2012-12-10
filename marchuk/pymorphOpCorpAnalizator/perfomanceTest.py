__author__ = 'amarch'
# -*- coding: utf-8 -*-

from opcorpTextProcessing import *
from pymorphyWrapper import *
import time

# Метод, меряющий точность реализованных анализаторов.
# Используются тексты (формат XML) со снятой омонимией, доступные на сайте Открытого корпуса.
# На 10 декабря 2012 года тексты содержали примерно предложений: 2724, токенов: 14005, слов: 7520.
# Итоговая оценка рассчитывается как для вероятностного алгоритма: если метод угадывает форму слова и его характеристики,
# то к оценке добавляется 1/len(vlist), где vlist - список возможных вариантов, выданных анализатором. По сути это
# вероятность угадать правильный ответ.

def perfomanceTest(sentnum):
    print 'Perfomance test start.'
    start_time = time.time()
    sentences =  getSentencesFromXML("/home/amarch/Documents/CSCenter/Python/corpus/annot.opcorpora.no_ambig.xml", sentnum)
    morph = POCMorph('/home/amarch/Downloads/ru.sqlite-json','/home/amarch/Documents/CSCenter/Python')
    finish_sent_time = time.time()
    pymorphy_points = 0
    pocmorph_points = 0
    opc_points = 0
    pytime = 0
    poctime = 0
    opctime = 0
    toknumber = 0

    for sent in sentences:
        for tokens in sent[1:]:
            for token in tokens:
                toknumber += 1
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

    print 'Time: prepare ',len(sentences),' sentences during', finish_sent_time - start_time, "seconds"
    print 'Number of tokens: ', toknumber
    print 'Total time: ', time.time() - start_time


# Пример использования:
if __name__ == "__main__":
    # Померить точность работы и время на первых 10 предложениях
    perfomanceTest(10)