__author__ = "Liana Bakradze"

from sys import argv

def encrypt():
	"""
		Encrypts open text with the key given.
		File with key format:
			the first row: the alphabet without gaps
			the second row: the key written under the letter it substitutes
	"""
	keyFile = open(argv[2], "r")
	letters = keyFile.readline().strip()
	chipher = keyFile.readline().strip()
	keyFile.close()
	keys = {}
	for i in xrange(len(letters)):
		keys[letters[i]] = chipher[i]
	f = open(argv[1], "r")
	g = open("ciphertext.txt", "w")
	data = f.read()
	temp = data.lower()
	encryptedData = ""
	for i in temp:
		if i in keys:
			encryptedData += keys[i]
		else:
			encryptedData += i
	g.write(encryptedData)
	f.close()
	g.close()

if __name__ == "__main__":
	encrypt()
