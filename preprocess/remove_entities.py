import csv
import subprocess
import string
import re
import time
from stem import IndonesianStemmer
from suds.client import Client

def _removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

keyword_penyakit = "ispa"

directory = '../dataset/' + keyword_penyakit + '/'

postfixes = [{'hashtags':'#'}, {'media':''}, {'mentions':'@'}, {'urls':''}]
entity_dict = {}

scan_class = True

if scan_class:
	class_dict = {}
	with open('../training/labels_all.csv', 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			class_dict[row['id']] = row['class']

#save tweets as dictionary
tweets = []
with open(directory + keyword_penyakit + '.csv', 'r') as f:
	reader = csv.DictReader(f)
	for row in reader:
		if not scan_class:
			if 'class' not in row or row['class'] == '':
				row['class'] = '?'
		else:
			if row['id'] in class_dict:
				row['class'] = class_dict[row['id']]
			else:
				row['class'] = ''
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

#web service to remove stopwords
#soap_url = "http://fws.cs.ui.ac.id/StopwordRemover/StopwordRemover"
#wsdl_url = "http://fws.cs.ui.ac.id/StopwordRemover/StopwordRemover?wsdl"
#client_stopwords = Client(url=wsdl_url, location=soap_url)
stopwords_file = open('stopwords.txt', 'r')
stopwords = [x.rstrip() for x in stopwords_file]

#web service for stemming
#soap_url = "http://fws.cs.ui.ac.id/Stemmer/Stemmer"
#wsdl_url = "http://fws.cs.ui.ac.id/Stemmer/Stemmer?wsdl"
#client_stemmer = Client(url=wsdl_url, location=soap_url)
stemmer = IndonesianStemmer()

f = open(directory + keyword_penyakit + '_preprocessed.csv', 'w')
writer = csv.writer(f)
writer.writerow(['id','text_original','text_formal','entity','class'])
f.close()

tweet_result = []
for tweet in tweets:
	text = tweet['text']
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

	text = "\'" + " ".join(tokens) + "\'"

	text_formal = subprocess.check_output(["java", "Formalizer", " ".join(tokens)])
	#text_formal = client_stopwords.service.removeStopword(text_formal)
	tokens = text_formal.split()
	tokens = [x for x in tokens if x not in stopwords]
	tokens_stem = [stemmer.stem(x) for x in tokens]
	text_formal = " ".join(tokens_stem)
	#text_formal = client_stemmer.service.StemSentence(text_formal)
	#time.sleep(1)

	for entity in entities:
		if entity.startswith('#'):
			text_formal = text_formal + ' ' + entity
			
	try:
		text_formal = "\'" + text_formal.strip() + "\'"
	except:
		text_formal = "";

	
	print tweet['id'] + ": " + text_formal

	tweet_result.append({'id':tweet['id'], 'text_original':tweet['text'], 'text_formal':text_formal, 'entity':" ".join(entities), 'class':tweet['class']})

	#write to file
	f = open(directory + keyword_penyakit + '_preprocessed.csv', 'a')
	writer = csv.writer(f)
	writer.writerow([tweet['id'], tweet['text'], text_formal, " ".join(entities), tweet['class']])
	f.close()


#write to file
'''with open(directory + keyword_penyakit + '_entities_processed.csv', 'w') as f:
	writer = csv.writer(f)

	writer.writerow(['id','text','text_formal','entity','class'])
	for tweet in tweet_result:
		writer.writerow([tweet['id'], tweet['text'], tweet['text_formal'], tweet['entity'], tweet['class']])'''











