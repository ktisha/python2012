__author__ = "amarch"
# -*- coding: utf-8 -*-

from lxml import etree

# Метод, извлекающий из текстов со снятой омонимией в формате XML (например [http://opencorpora.org/?page=downloads])
# прдложения и характеристики слов с помощью XPath. В качестве аргументов используется путь до файла с тестами и количество
# извлекаемых предложений (если указано больше чем возможно - извлекается сколько возможно, по умолчанию извлекаются все).
# Итоговый список имеет формат списка для всех предложений, где каждое предложение хранится как
# ['предложение', [{'norm','info','class'}, 'token']], т.е. текст предложения и информация для всех токенов.

def getSentencesFromXML(filepath, sentencesno = 0):
    tree = etree.parse(filepath)
    sentences = []
    if sentencesno < 0:
        return sentences
    else:
        id_sentences = tree.xpath("//text/paragraphs/paragraph/sentence/@id")
        if sentencesno > 0:
            q = min(len(id_sentences), sentencesno)
            id_sentences = id_sentences[0:q]
        for id in id_sentences:
            tmp = []
            quer = ''.join(["//text/paragraphs/paragraph/sentence[@id = ",id,"]/source/text()"])
            tmp.append(tree.xpath(quer))
            quer = ''.join(["//text/paragraphs/paragraph/sentence[@id = ",id,"]/tokens/token/@id"])
            tokens_id = tree.xpath(quer)
            tokens = []
            for t in tokens_id:
                token = []
                quer = ''.join(["//text/paragraphs/paragraph/sentence[@id = ",id,"]/tokens/token[@id=",t,"]/@text"])
                token.append(tree.xpath(quer)[0])
                quer = ''.join(["//text/paragraphs/paragraph/sentence[@id = ",id,"]/tokens/token[@id=",t,"]/tfr/v/l/@t"])
                norm = tree.xpath(quer)
                quer = ''.join(["//text/paragraphs/paragraph/sentence[@id = ",id,"]/tokens/token[@id=",t,"]/tfr/v/l/g[1]/@v"])
                clas = tree.xpath(quer)
                quer = ''.join(["//text/paragraphs/paragraph/sentence[@id = ",id,"]/tokens/token[@id=",t,"]/tfr/v/l/g/@v"])
                info = tree.xpath(quer)
                info = info[1:]
                info = map(unicode, info)
                token.append({'class':unicode(clas[0],'utf-8'), 'norm':norm[0], 'info':info})
                tokens.append(token)
            tmp.append(tokens)
            sentences.append(tmp)
        return sentences

# Примеры использования
if __name__ == "__main__":

    # Извлечение первого предложения и информации о содержащихся токенах в список.
    sentences =  getSentencesFromXML("/home/amarch/Documents/CSCenter/Python/corpus/files/export/annot/small.xml", 1)
    print sentences[1]


