import numpy as np
from collections import Counter

def entropy(y):

	size = len(y)
	diff = np.unique(y)
	count = [0]*len(diff)
	for i in range(len(diff)):
		for j in range(size):
			if diff[i] == y[j]:
				count[i] += 1

	ent = 0
	for i in range(len(count)):
		p = count[i]/size
		if p > 0:
			ent += -p * np.log2(p)
	return ent

class Node:

	def __init__(self,feature = None, threshold = None, left = None, right = None,*,value=None):
		self.feature = feature
		self.threshold = threshold
		self.left = left
		self.right = right
		self.value = value

	def isLeafNode(self):
		return self.value is not None

class DecisionTree:

	def __init__(self, maxDepth=10):
		self.minSampleSplit = 2
		self.maxDepth = maxDepth
		self.numberOfFeatures = None
		self.root = None

	def fit(self, x,y):
		
		if not self.numberOfFeatures:
			self.numberOfFeatures = x.shape[1]

		else:
			min(self.numberOfFeatures, X.shape[1])
		
		self.root = self.addNode(x,y)

	
	def addNode(self,x,y, depth=0):

		nSamples, nFeatures = x.shape
		nLables = len(np.unique(y))

		if depth >= self.maxDepth or nLables == 1 or nSamples < self.minSampleSplit:
			leafValue = self._mostCommonLabel(y)
			return Node(value = leafValue)

		featureIndex = np.random.choice(nFeatures, self.numberOfFeatures, replace=False)


		bestFeatures, bestThreshold = self.bestParameters(x,y, featureIndex)
		leftIndex, rightIndex = self.split(x[:, bestFeatures], bestThreshold)
		left = self.addNode(x[leftIndex, :],y[leftIndex], depth+1)
		right = self.addNode(x[rightIndex, :],y[rightIndex], depth+1)

		return Node(bestFeatures, bestThreshold, left, right)

	def bestParameters(self,x,y,featIndex):
		bestGain = -1
		splitIndex = None
		splitThreshold = None

		for index in featIndex:
			featureVector = x[:,index]
			thresholds = np.unique(featureVector)
			for threshold in thresholds:
				gain = self.informationGain(y,featureVector,threshold)
				if gain > bestGain:
					bestGain = gain
					splitIndex = index
					splitThreshold = threshold

		return splitIndex, splitThreshold

	def informationGain(self, y, featureVector, splitThresh):
		labelEntropy = entropy(y)
		
		left, right = self.split(featureVector, splitThresh)

		if len(left) == 0 or len(right) == 0:
			return 0

		n = len(y)
		nLeft, nRight = len(left), len(right)
		leftEntropy, rightEntropy = entropy(y[left]), entropy(y[right])
		childNodesEntropy = (nLeft/n) * leftEntropy + (nRight/n) * rightEntropy

		# return gain
		informationGain = labelEntropy - childNodesEntropy
		return informationGain


	def split(self, featureVector, splitThresh):
		leftIndex = np.argwhere(featureVector <= splitThresh).flatten()
		rightIndex = np.argwhere(featureVector > splitThresh).flatten()

		return leftIndex, rightIndex

	def _mostCommonLabel(self,y):

		counter = Counter(y)
		mostCommon = counter.most_common(1)[0][0]
		return mostCommon

	def predict(self, x):
		return np.array([self._traverse(x1, self.root) for x1 in x])

	def _traverse(self,x, node):
		if node.isLeafNode():
			return node.value

		if x[node.feature] <= node.threshold:
			return self._traverse(x,node.left)
		return self._traverse(x,node.right)
