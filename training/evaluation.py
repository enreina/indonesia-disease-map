from sklearn.metrics import f1_score, precision_score, recall_score
import numpy as np
import csv
from sklearn.feature_extraction.text import CountVectorizer


#read tweets and vectorize words
keyword_penyakit = "ispa"

directory = '../dataset/' + keyword_penyakit + '/'

#save tweets
tweets = []
with open(directory + keyword_penyakit + '_labeled.csv', 'r') as f:
	reader = csv.DictReader(f)
	for row in reader:
 		tweets.append(row)

#store labels
temp = []
for tweet in tweets:
	if tweet['class'] == keyword_penyakit:
		temp.append(1)
	elif tweet['class'] == 'neg':
		temp.append(0)
	else:
		temp.append(None)

label_predicted = np.array(temp,np.float)
labels = np.zeros(len(tweets))

tweet_indices = np.random.choice(len(tweets),50)

print "asking labels..."
for idx in tweet_indices:
	print tweets[idx]['id'] + ": " + tweets[idx]['text_original']
	label = input("input label: ")
	labels[idx] = label

print "precision: " + str(precision_score(labels[tweet_indices], label_predicted[tweet_indices]))
print "recall: " + str(recall_score(labels[tweet_indices], label_predicted[tweet_indices]))
print "f1: " + str(f1_score(labels[tweet_indices], label_predicted[tweet_indices]))
