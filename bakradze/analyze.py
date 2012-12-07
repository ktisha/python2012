from sys import argv
from encryptor import encrypt
keys = {}
freqBigramsUnfound = []
freqBigramsFound = 0
def findBigram(input, output, CALIBRE):
	f = open(input, "r")
	data = f.read()
	f.close()
	temp = filter(lambda x: x.isalpha() or x in " \n\t", data)
	freq = {}
	for i in xrange(len(temp) - 1):
		if temp[i] in ' \n\t' or temp[i+1] in ' \t\n':
			continue
		try: 
			freq[temp[i] + temp[i+1]] +=1 
		except:
			freq[temp[i] + temp[i+1]] = 1
	freq = sorted(freq.iteritems(), key = lambda (k,v):(-v, k))
	keyFile = open("freq.txt", "r")
	alphabet = keyFile.readline().strip()
	chipher = keyFile.readline().strip()
	keyFile.close()
	for i in xrange(len(alphabet)):
		keys[alphabet[i]] = chipher[i]
	bigrams = ' ' + open("bigramfreq.txt", "r").read() + ' '
		
	def bigramUpdate():
		global freqBigramsUnfound
		global freqBigramsFound
		global keys
		freqDecrypted = {}
		for key, value in freq:
			freqDecrypted[keys[key[0]] + keys[key[1]]] =  value
		freqDecrypted = sorted(freqDecrypted.iteritems(), key = lambda (k,v):(-v, k))[:CALIBRE]
		freqBigramsFound = 0
		freqBigramsUnfound = []
		for key, value in freqDecrypted:
			if key in bigrams:
				freqBigramsFound += 1
			else:
				freqBigramsUnfound.append(key)

	def improveKey(curBigram):
		for n in xrange(2):
			c = curBigram [n]
			i = chipher.index(c)
			for di in (1, -1, 2, -2, 3, -3):
				if (-1 < i + di < len(chipher)):
					keys[alphabet[i]] = chipher[i + di]
					keys [alphabet[i + di]] = chipher[i]
					temp = ''.join(map(lambda x : keys[alphabet[i]] if x == c else x, curBigram))
					if temp in bigrams:
						return True
					else:
						keys[alphabet[i]] = chipher[i]
						keys[alphabet[i + di]] = chipher[i + di]
		return False
	
	def improveBigram(i):
		global keys
		oldKey = keys.copy()
		if not improveKey(i):
			return
		freqDecrypted = {}
		for key, value in freq:
			freqDecrypted[keys[key[0]] + keys[key[1]]] =  value
		freqDecrypted = sorted(freqDecrypted.iteritems(), key = lambda (k,v):(v, k))[-CALIBRE:]
	        count = 0
		for key, value in freqDecrypted:
			if key in bigrams:
				count += 1
		if count < freqBigramsFound:
			keys = oldKey.copy()
		else:
			bigramUpdate()
	
	bigramUpdate()		
	while freqBigramsUnfound:
		improveBigram(freqBigramsUnfound.pop())
	g = open("newKey.txt", "w")
	g.write(alphabet + "\n")
	for i in alphabet:
		g.write(keys[i])
	g.close()	
	encrypt(input, output, "newKey.txt")

if __name__ == "__main__":
	findBigram(argv[1], argv[2], int(argv[3]))
