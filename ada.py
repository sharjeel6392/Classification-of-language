from dtree import DecisionTree
import numpy as np


class adaBoost:
	def __init__(self, classifiers=5):
		self.classifiers = classifiers

	def fit(self, X, Y):
		self.models = []
		self.hypotheses = []

		N = X.shape[0]

		for classifier in range(self.classifiers):
			W = np.ones(N) / N
			err = 0
			weakClassifier = DecisionTree(maxDepth=1)
			weakClassifier.fit(X, Y)
			
			P = weakClassifier.predict(X)

			for e in range(N):
				if Y[e] != P[e]:
					err += W[e]

			alpha = 0.5*(np.log(1 - err) - np.log(err))

			for i in range(len(Y)):
				if P[i] == Y[i]:
					W[i] = W[i] * np.exp(-alpha)
				else:
					W[i] = W[i] * np.exp(alpha)

			W = W/np.sum(W)

			X_new = X
			y_new = Y
			indexNew = 0
			while indexNew < len(X):
				r = np.random.random(1)[0]
				tempSum = 0
				for i in range(len(W)):

					tempSum += W[i]
					if tempSum > r:
						break

				X_new[indexNew] = X[i]
				y_new[indexNew] = Y[i]
				indexNew += 1

			X = X_new
			Y = y_new
			self.models.append(weakClassifier)
			self.hypotheses.append(alpha)
			

	def predict(self, X):
		N = len(X)
		y_pred = np.zeros(N)
		for alpha, weakClassifier in zip(self.hypotheses, self.models):
			y_pred += alpha*weakClassifier.predict(X)

		for i in range(N):
			if y_pred[i] < 0:
				y_pred[i] = -1
			elif y_pred[i] == 0:
				y_pred[i] = 0
			else:
				y_pred[i] = 1
		return y_pred
