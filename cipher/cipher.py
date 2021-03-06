def make_cipher(all_text):
	from string import lowercase,maketrans
	from random import shuffle
	lowercase_perm = list(lowercase)
	shuffle(lowercase_perm)
	cipher_table = maketrans(lowercase,''.join(lowercase_perm))
	all_ciphered_text = []
	for text in all_text: 
		ciphered_text = text.translate(cipher_table)
		all_ciphered_text.append(ciphered_text)
	return all_ciphered_text

def write_cipher(text_filename, cipher_filename):
	from string import punctuation
	#input = open(text_filename,'r')
	text = []
	input = open(text_filename,"r");
	lines = input.readlines();
	for i in lines:
		thisline = i.lower().translate(None,punctuation+'\n').split(" ");
		text += thisline
	ciphered_text = make_cipher(text)
	output = open(cipher_filename,'w')
	for word in ciphered_text:
		output.write(word+" ");
	output.close();
