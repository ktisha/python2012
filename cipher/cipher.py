def make_cipher(text):
	from string import lowercase,maketrans
	from random import shuffle
	lowercase_perm = list(lowercase)
	shuffle(lowercase_perm)
	cipher_table = maketrans(lowercase,''.join(lowercase_perm))
	ciphered_text = text.translate(cipher_table)
	return ciphered_text

def write_cipher(text_filename, cipher_filename):
	from string import punctuation
	input = open(text_filename,'r')
	text = input.read().lower().translate(None,punctuation+' '+'\n')
	ciphered_text = make_cipher(text)
	output = open(cipher_filename,'w')
	output.write(ciphered_text);