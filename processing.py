import nltk
import random
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

pos = open("positive.txt","r").read()
neg = open("negative.txt","r").read()

doc=[]
all_words=[]

for p in pos.split('\n'):
    doc.append((p, 'positif'))
    words = word_tokenize(p)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in ['J','R','V']:
            all_words.append(w[0].lower())

    
for p in neg.split('\n'):
    doc.append((p, 'negatif'))
    words = word_tokenize(p)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in ['J','R','V']:
            all_words.append(w[0].lower())
    
save_doc = open("pickled/doc.pickle","wb")
pickle.dump(doc, save_doc)
save_doc.close()

all_words=nltk.FreqDist(all_words)

w_features=list(all_words.keys())[:5000]

save_w_features = open("pickled/w_features.pickle","wb")
pickle.dump(w_features, save_w_features)
save_w_features.close()


def find_features(document):
    words = word_tokenize(document)
    features={}
    for word in w_features:
        features[word]=(word in words)
    return features

featuresets=[(find_features(l),category) for (l,category) in doc]

random.shuffle(featuresets)

save_featuresets = open("pickled/featuresets.pickle","wb")
pickle.dump(featuresets, save_featuresets)
save_featuresets.close()

training_set=featuresets[:10000]
testing_set=featuresets[10000:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)

save_classifier = open("pickled/classifier.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

def score(text):
	f=find_features(text)
	return classifier.classify(f)
