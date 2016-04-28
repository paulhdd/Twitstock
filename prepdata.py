import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

file_path='/Users/phd/Downloads/trainingandtestdata/training.1600000.processed.noemoticon.csv'

tweet_frame=pd.read_csv(file_path,header=None,usecols=[0,5],names=['rate','text'])

doc=[]
all_words=[]
stop_words = set(stopwords.words('english'))

for el in tweet_frame.values:
	if  el[0]==4:
		doc.append((el[1], 'positif'))
		words = word_tokenize(el[1])
    	for w in words:
     		if w.isalpha():
       			all_words.append(w.lower())
	elif el[0]==0:
		doc.append((el[1], 'negatif'))
   		words = word_tokenize(el[1])
    	for w in words:
     		if w.isalpha():
       			all_words.append(w.lower())