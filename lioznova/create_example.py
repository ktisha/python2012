import sys
from string import maketrans
from random import shuffle

def make_abrakadabra(text, alphabet):  
    array = range(0, len(alphabet))  
    shuffle(array)  
    abrakadabra=""
    for i in range(0, len(alphabet)):  
        abrakadabra += alphabet[array[i]]
    intab  = alphabet
    outtab = abrakadabra
    trantab = maketrans(intab, outtab)
    return text.translate(trantab)

file_to_decode = sys.argv[1]
text_file = open(file_to_decode, 'r')
text_to_decode = text_file.read()
text_file.close()
text_to_decode = text_to_decode.lower()
output_file = open('./example.txt','w')
output_file.write(make_abrakadabra(text_to_decode, "abcdefghijklmnopqrstuvwxyz"))
output_file.close()
