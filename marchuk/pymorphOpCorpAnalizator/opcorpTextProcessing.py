__author__ = "amarch"
# -*- coding: utf-8 -*-

from lxml import etree

def getSentences_fromXML(filepath, sentencesno=0):
    tree = etree.parse(filepath)
    sentences = []
    if sentencesno < 0:
        return sentences
    else:
        id_sentences = tree.xpath("//text/paragraphs/paragraph/sentence/@id")
        if sentencesno > 0:
            id_sentences = id_sentences[0:min(len(id_sentences), sentencesno)]
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
                token.append({'class':unicode(clas[0],'utf-8'), 'norm':norm[0], 'info':info})
                tokens.append(token)
            tmp.append(tokens)
            sentences.append(tmp)
        return sentences

if __name__ == "__main__":
    sentences =  getSentences_fromXML("/home/amarch/Documents/CSCenter/Python/corpus/files/export/annot/small.xml")



