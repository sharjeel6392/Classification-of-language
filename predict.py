import sys
import pickle

import numpy as np

from dataParsing import get_features
from dtree import DecisionTree
from ada import adaBoost


def clean(line):
	sent = ''
	sent2 = []
	for i in range(len(line)):
		c = line[i].lower()
		if c==',' or c=='.' or c=="(" or c==')' or c=='-':
			sent += ' '
		else:
			sent += line[i]
	return sent

def readFile(file, flag=None):
	f = open(file)
	features = []
	label = []
	for line in f:
		line.strip()
		if flag:
			label.append(line[:2])
			line = line[3:]
		line = clean(line)
		temp = get_features(line)
		features.append(temp)
	if flag:
		return features, label
	else:
		return features

def TFMatrix(features):
	featureMat = []
	for feature in features:
		temp = []
		for key in feature:
			temp.append(feature[key])
		featureMat.append(temp)

	return featureMat

def printPrediction(y):
	for item in y:
		if item == '0' or item == '-1' or item == 0 or item == -1:
			print("nl")
		else:
			print("en")

def main():
	
	if len(sys.argv) != 3:
		print("Invalid number of arguments.")
		sys.exit(0)

	hypothesis, file = sys.argv[1],sys.argv[2]
	
	obj = open(hypothesis,'rb')
	classifier = pickle.load(obj)

	f = readFile(file)
	X_test = np.array(TFMatrix(f))

	y_pred = classifier.predict(X_test)
	
	printPrediction(y_pred)

if __name__ == '__main__':
	main()
