from encryptor import encrypt
from sys import argv

def crack(input, output):
	f = open(input, "r")
	data = f.read()
	f.close()
	temp = filter(lambda x: x.isalpha(), data)
	freq = {}
	for i in "abcdefghijklmnopqrstuvwxyz":
		freq[i] = 0
	for c in temp:
		freq[c] += 1
	freq = sorted(freq.iteritems(), key = lambda (k,v):(-v, k))
	letters = "\netaoinhsrdlumcwgfypbkvxjxz"
	g = open("freq.txt", "w")
	for key, value in freq:
		g.write(key)
	g.write(letters)
	g.close()
	encrypt(input, output,"freq.txt")

if __name__ == "__main__":
	crack(argv[1], argv[2])