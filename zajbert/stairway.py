# -*- coding: utf-8 -*-

import codecs



def createDict (sizeOfWord):
    with codecs.open('runouns.txt', 'r', 'utf-8') as oldDict:
        setOfUsefulWords = set()
        for word in oldDict:
            if len(word) - 2 == sizeOfWord: # отсекаем \r\n
                setOfUsefulWords.add(word[:-2])
        return setOfUsefulWords

def searchNewWords (word):
    global setOfUsefulWords
    global quequeToVisit
    global openWords
    global currentNumber
    global lastWord
    letters = u"абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    for i in xrange(len(word)):
        for ch in letters:
            newWord = word[0 : i] + ch + word[i + 1 : 100]
            if newWord == lastWord:
                openWords[newWord] = currentNumber
                return True
            if word == newWord or newWord in openWords:
                continue
            if newWord in setOfUsefulWords:
                quequeToVisit.append(newWord)
                openWords[newWord] = currentNumber
    return False

def itIsImpossible():
    with codecs.open('answer.txt', 'w', 'utf-8') as answerFile:
        answerFile.write('''it's impossible!!''')

with codecs.open('input.txt', 'r', 'utf-8') as f:
   firstWord = f.readline().replace('\n', '')
   lastWord = f.readline().replace('\n', '')

if firstWord == lastWord:
    with codecs.open('answer.txt', 'w', 'utf-8') as answerFile:
        answerFile.write(firstWord)

elif len(firstWord) != len(lastWord):
    itIsImpossible()
else:
    flagImpossible = False
    setOfUsefulWords = createDict(len(firstWord))
    quequeToVisit = []
    quequeToVisit.append(firstWord)
    openWords = {}  #this words we shouldn't add in queque, value = number of word, which we came from
    openWords[firstWord] = -1
    visitedWords = [firstWord]
    currentNumber = 0
    currentWord = firstWord
    while (not searchNewWords(currentWord)) and (not flagImpossible):
        if len(quequeToVisit) is  0:
            itIsImpossible()
            flagImpossible = True
            continue
        currentWord = quequeToVisit[0]
        del quequeToVisit[0]

        visitedWords.append(currentWord)
        currentNumber += 1

    if not flagImpossible:
        currentNumber = openWords[lastWord]
        with codecs.open('answer.txt', 'w', 'utf-8') as f:
            f.write(lastWord + '\n')
            while currentNumber != -1:
                word = visitedWords[currentNumber]
                f.write(word + '\n')
                currentNumber = openWords[word]