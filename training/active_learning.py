from sklearn.naive_bayes import GaussianNB
from sklearn import svm
import numpy as np
import csv
from sklearn.feature_extraction.text import CountVectorizer


#read tweets and vectorize words
keyword_penyakit = "ispa"

directory = '../dataset/' + keyword_penyakit + '/'

#save tweets
tweets = []
with open(directory + keyword_penyakit + '_preprocessed.csv', 'r') as f:
	reader = csv.DictReader(f)
	for row in reader:
 		tweets.append(row)
#vectorize tweet
countVectorizer = CountVectorizer()
tweet_vectors = countVectorizer.fit_transform([tweet['text_formal'] for tweet in tweets])

#store labels
temp = []
for tweet in tweets:
	if tweet['class'] == keyword_penyakit:
		temp.append(1)
	elif tweet['class'] == 'neg':
		temp.append(0)
	else:
		temp.append(None)

labels = np.array(temp,np.float)

#function definitions
def select_tweets(tweet_indices, classifier=None, k=10):
	if classifier is None:
		return np.random.choice(tweet_vectors[tweet_indices].shape[0],k)
	else:
		#select least confidence sample
		confidence = classifier.decision_function(tweet_vectors[tweet_indices])
		pos_indices = np.where(confidence > 0)[0]
		neg_indices = np.where(confidence < 0)[0]


		#select k/2 from positive samples
		sorted_indices = confidence[pos_indices].argsort()[:k/2]
		print confidence[pos_indices[sorted_indices]]
		pos_indices = tweet_indices[pos_indices[sorted_indices]]
		#select k/2 from negative samples
		sorted_indices = confidence[neg_indices].argsort()[-k/2:]
		print confidence[neg_indices[sorted_indices]]
		neg_indices = tweet_indices[neg_indices[sorted_indices]]

		return np.concatenate([pos_indices, neg_indices])

def ask_label(selected_indices, labeled_indices):
	print "asking labels..."
	for idx in selected_indices:
		print tweets[idx]['id'] + ": " + tweets[idx]['text_original']
		labels[idx] = input("input label: ")
		labeled_indices.append(idx)

#initialize labeled and unlabeled set
labeled_indices = []
unlabeled_indices = np.array(range(0, tweet_vectors.shape[0]))

classifier = svm.LinearSVC(class_weight='auto')

#active learning loop
min_confidence = 0
labels_enough = False
ii = 0
max_iter = 10
while min_confidence < 0.1 and ii < max_iter:
	if not labels_enough or len(labeled_indices) == 0:
		selected_indices = select_tweets(unlabeled_indices)
	else:
		selected_indices = select_tweets(unlabeled_indices, classifier)

	ask_label(selected_indices, labeled_indices)
	try:
		classifier.fit_transform(tweet_vectors[labeled_indices], labels[labeled_indices])
	except:
		labels_enough = False
		continue
	labels_enough = True
	confidence = classifier.decision_function(tweet_vectors[unlabeled_indices])
	min_confidence = np.absolute(confidence[np.where(confidence > 0)]).min()
	print "min confidence: ", min_confidence
	ii = ii + 1

labels = classifier.predict(tweet_vectors)
f = open(directory + keyword_penyakit + '_labeled.csv', 'w')
writer = csv.writer(f)
writer.writerow(['id','text_original','text_formal','entity','class'])
f.close()

for label,tweet in zip(labels.tolist(),tweets):
	if label is not None:
		if label == 0:
			tweet['class'] = 'neg'
		else:
			tweet['class'] = keyword_penyakit

	f = open(directory + keyword_penyakit + '_labeled.csv', 'a')
	writer = csv.writer(f)
	writer.writerow([tweet['id'], tweet['text_original'], tweet['text_formal'], tweet['entity'], tweet['class']])
	f.close()






