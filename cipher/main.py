from sys import argv
from cipher import *
from freq_counter import *
from string import lowercase,maketrans,punctuation

write_cipher(argv[1],argv[2])
chiphered_text_file = open(argv[2])
letters_frequency = all_letters_frequency(argv[2])
pair_frequency2 = all_pairs_of_letter_frequency(argv[2])
pair_frequency = all_pairs_of_letter_frequency(argv[1])
double = all_double_letters_frequency(argv[1])
print double
print pair_frequency[0:50]
right_letter_order = "ETAONRISHDLFCMUGYPWBVKJXQZ"
print "TH HE AN RE ER IN ON AT ND ST ES EN OF TE ED OR TI HI AS TO"
print "LL EE SS OO TT FF RR NN PP CC"
right_letter_order = right_letter_order.lower()

all_letters = []
for pairs in letters_frequency:
	letter,freq = pairs
	all_letters += [letter]
ciphered_letter_order = ''.join(str(l) for l in all_letters)
right_letter_order = right_letter_order[0:len(ciphered_letter_order)]
cipher_table = maketrans(ciphered_letter_order,right_letter_order)
ciphered_text = []
input = open(argv[2],"r");
lines = input.readlines();
for i in lines:
	ciphered_text += i.split(" ")

unciphered_text = [] 	
	
for word in ciphered_text:
	unciphered_text += [word.translate(cipher_table)]
output = open(argv[3],'w')
j=0
for word in unciphered_text:
	output.write(word+" ")
	j=j+1
	if(j%10 == 0):
		output.write('\n')
output.close()	
