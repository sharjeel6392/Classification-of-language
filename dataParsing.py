
def get_features(line):
	vowelPairs, conPairs = vowelConsPairs(line)

	words = set(line.split())

	features = {
				"cvRatio":		vowelConsRatio(line),
				"averageLen":	avgWordLen(line),
				"vowelPairs":	vowelPairs,
				"conPairs"	:	conPairs,
				"letterPairs":	letterPairs(line),
				"endsInEN"	:	endsIn("en",line),
				"containsHET":	0 if "het" in words else 1,
				"containsDE":	0 if "de" in words else 1,
				"containsOF":	1 if "of" in line else 0,
				"containsTHE":	1 if "the" in line else 0,
				"containsAND":	1 if "and" in line else 0,
			}
	return features


def vowelConsPairs(line):

	vowels = ("a","e","i","o","u")
	vCount = cCount = 0
	index = 0
		
	while index < len(line)-1:
		char = line[index]
		nextChar = line[index+1]

		if char in vowels and char == nextChar:
			vCount += 1
			index += 2
		elif char == nextChar:
			cCount += 1
			index += 2
		else:
			index += 1
	if vCount > 2:
		V = 0
	else:
		V = 1
	if cCount > 2:
		C = 1
	else:
		C = 0
	return V,C



def vowelConsRatio(line):
	vowels = ("a","e","i","o","u")
	vCount = cCount = 0

	for char in line:
		if char in vowels:
			vCount += 1
		else:
			cCount += 1

	ratio = vCount/cCount
	ratio *= 100	
	if int(ratio) > 40:
		return 0
	else:
		return 1


def avgWordLen(line):

	totalCount = 0

	for words in line:
		if words.isdigit():
			pass
		else:
			totalCount += 1

	avg = totalCount // len(line.split())

	if avg > 3:
		return 0
	else:
		return 1


def endsIn(string,line):
	line = line.split()
	for word in line:
		if len(word) < len(string):
			continue

		diff = len(word) - len(string)
		flag = 1

		for char in string:
			if word[diff] != char:
				flag = 0
				break
			diff += 1
		if flag:
			return flag

	return 0


def letterPairs(line):
	
	count = 0
	for i in range(len(line)-1):
		char = line[i]
		nextChar = line[i+1]

		if char == nextChar:
			count += 1
	if count > 3:
		return 0
	else:
		return 1
