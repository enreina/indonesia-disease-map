import csv
import json
import string
import re
import time
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import DBSCAN

#read tweets and vectorize words
keyword_penyakit = "dbd"

directory = '../dataset/' + keyword_penyakit + '/'


tweets_created_at = {}
with open(directory + keyword_penyakit + '.csv', 'r') as f:
	reader = csv.DictReader(f)
	for row in reader:
		tweets_created_at[row['id']] = row['created_at']

tweets_orig = []
with open(directory + keyword_penyakit + '_geo.csv', 'r') as f:
	reader = csv.DictReader(f)
	for row in reader:
		row['created_at'] = time.strptime(tweets_created_at[row['id']], "%Y-%m-%d %H:%M:%S")
 		tweets_orig.append(row)

#sort tweets based on created at
tweets_orig.sort(key=lambda tweet: tweet['created_at'])


f = open(directory + keyword_penyakit + '_geo_similarity.csv', 'w')
writer = csv.writer(f)
writer.writerow(['id','created_at','text_original','text_formal','entity','location_name','geo_lat', 'geo_lng', 'class'])
f.close()

countVectorizer = CountVectorizer()
tweet_vectors = countVectorizer.fit_transform([tweet['text_formal'] for tweet in tweets_orig])

distance_matrix = pairwise_distances(tweet_vectors.toarray(), metric='jaccard')

#iterate i,j
eps = 0.5
for i in range(0,len(tweets_orig)):
	j = i + 1
	while j < len(tweets_orig):
		if tweets_orig[j] != {} and tweets_orig[i] != {} and distance_matrix[i,j] < eps:
			print i,": ",tweets_orig[i]['text_original']
			print j,": ",tweets_orig[j]['text_original']
			print 'similarity',distance_matrix[i,j]
			tweets_orig[j] = {}
		else:
			j = j + 1

tweets_orig = [tweet for tweet in tweets_orig if tweet != {}]

for row in tweets_orig:
	f = open(directory + keyword_penyakit + '_geo_similarity.csv', 'a')
	writer = csv.writer(f)
	writer.writerow([row['id'], time.strftime("%Y-%m-%d %H:%M:%S",row['created_at']),row['text_original'], row['text_formal'], row['entity'], row['location_name'], row['geo_lat'], row['geo_lng'], row['class']])
	f.close()


'''deduplication with DBSCAN
db = DBSCAN(eps=0.2,metric='precomputed').fit(distance_matrix)
print db.labels_
unique_labels = set(db.labels_)

clusters = {}
for i in unique_labels:
	clusters[i] = []


for i in range(0,len(tweets_orig)):
	row = tweets_orig[i]
	clusters[db.labels_[i]].append(row)

for label in clusters:
	if len(clusters[label]):
		row = clusters[label][0]
		f = open(directory + keyword_penyakit + '_geo_similarity.csv', 'a')
		writer = csv.writer(f)
		writer.writerow([row['id'], row['text_original'], row['text_formal'], row['entity'], row['location_name'], row['geo_lat'], row['geo_lng'], row['class'], db.labels_[i]])
		f.close()
'''
	



