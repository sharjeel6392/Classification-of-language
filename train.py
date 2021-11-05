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

def main():
	examples, hypothesisOut, LearningType = sys.argv[1], sys.argv[2], sys.argv[3]
	
	f,y_train = readFile(examples,True)
	X_train = np.array(TFMatrix(f))
	y_train = np.array(y_train)

	file = open(hypothesisOut, 'wb')
	
	if LearningType == 'dt':
		maxDepth = int(input("Depth of the tree (<8): "))
		for i in range(len(y_train)):
			if y_train[i] == 'nl':
				y_train[i] = 0
			elif y_train[i] == 'en':
				y_train[i] = 1
				
		classifier = DecisionTree(maxDepth=maxDepth)
		classifier.fit(X_train,y_train)
		pickle.dump(classifier, file)

	elif LearningType == 'ada':
		stumps = int(input("Number of stumps: "))
		trainLable = np.ones(len(y_train))
		for i in range(len(y_train)):
			if y_train[i] == 'nl':
				trainLable[i] = -1
			elif y_train[i] == 'en':
				trainLable[i] = 1

		classifier = adaBoost(classifiers=stumps)
		classifier.fit(X_train,trainLable)
		pickle.dump(classifier, file)

	print("Training Done!")


if __name__ == '__main__':
	main()
