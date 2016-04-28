import nltk
import random
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from nltk.classify.scikitlearn import SklearnClassifier


docf = open("pickled/doc.pickle", "rb")
doc= pickle.load(docf)
docf.close()


w_ff= open("pickled/w_features.pickle", "rb")
w_features = pickle.load(w_ff)
w_ff.close()

def find_features(document):
    words=set(document)
    features={}
    for word in w_features:
        features[word]=(word in words)
    return features

featuresets=[(find_features(l),category) for (l,category) in doc]

featuresetsf = open("pickled/featuresets.pickle", "rb")
featuresets = pickle.load(featuresetsf)
featuresetsf.close()


classifierf = open("pickled/classifier.pickle","rb")
classifier=pickle.load(classifierf)
classifierf.close()

def score(text):
	features=find_features(text)
	return classifier.classify(features)
