import csv
import subprocess
import string
import re
import time
from collections import Counter

def _removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def _findCommonCooccur(search_word, tweets):
	count_search = Counter()
	for tweet in tweets:
		text = tweet['text']
		terms_only = text.split()
		if search_word in terms_only:
			count_search.update(terms_only)
	print "Co-occurence for %s: " % search_word
	print count_search.most_common(20)

keyword_penyakit = "dbd"

queries = ['dbd', 'demam', 'dengue']

directory = '../dataset/' + keyword_penyakit + '/'

postfixes = [{'hashtags':'#'}, {'media':''}, {'mentions':'@'}, {'urls':''}]
entity_dict = {}

#save tweets as dictionary
tweets = []
with open(directory + keyword_penyakit + '_labeled.csv', 'r') as f:
	reader = csv.DictReader(f)
	for row in reader:
		if row['class'] == keyword_penyakit:
 			tweets.append(row)

#save entities to their own dictionary for each tweet
for postfix in postfixes:
	with open(directory + keyword_penyakit + "_" + postfix.keys()[0] + ".csv", 'r') as f:
		next(f, None)
		reader = csv.reader(f,delimiter=',')
		for row in reader:
			if row[0] not in entity_dict:
				entity_dict[row[0]] = [postfix.values()[0] + row[1]]
			else:
				entity_dict[row[0]].append(postfix.values()[0] + row[1])

stopwords_file = open('stopwords.txt', 'r')
stopwords = [x.rstrip() for x in stopwords_file]

tweet_result = []
for tweet in tweets:
	text = tweet['text_original']
	#remove entities
	if tweet['id'] in entity_dict:
		entities = entity_dict[tweet['id']]
		for entity in entities:
			text = text.replace(entity, '')
	else:
		entities = []

	text = re.sub(r"http\S+", "", text)

	text = text.lower().replace('\n','').replace('\r','').replace("\"", " ")


	for c in string.punctuation:
		text = text.replace(c," ")

	text = re.sub(r"^\d+\s|\s\d+\s|\s\d+$", " ", text)

	text = re.sub(r"\brt\b", "", text)

	text = text.strip()

	text = _removeNonAscii(text)

	tokens = text.split()

	tokens = [x for x in tokens if not x.isdigit()]
	tokens = [x for x in tokens if x not in stopwords]

	if tweet['id'] in entity_dict:
		entities = entity_dict[tweet['id']]
		for entity in entities:
			if entity[0] == '#':
				text = text + ' ' + entity

	print tweet['id'] + ": " + text

	tweet_result.append({'id':tweet['id'], 'text':text})

for query in queries:
	_findCommonCooccur(query, tweet_result)


#write to file
'''with open(directory + keyword_penyakit + '_entities_processed.csv', 'w') as f:
	writer = csv.writer(f)

	writer.writerow(['id','text','text_formal','entity','class'])
	for tweet in tweet_result:
		writer.writerow([tweet['id'], tweet['text'], tweet['text_formal'], tweet['entity'], tweet['class']])'''











