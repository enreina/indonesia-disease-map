import csv
import json
from polyglot.text import Text

#read tweets and vectorize words
keyword_penyakit = "ispa"

directory = '../dataset/' + keyword_penyakit + '/'

tweets_orig = {}
with open(directory + keyword_penyakit + '.csv', 'r') as f:
	reader = csv.DictReader(f)
	for row in reader:
 		tweets_orig[row['id']] = row

f = open(directory + keyword_penyakit + '_geo.csv', 'w')
writer = csv.writer(f)
writer.writerow(['id','text_original','text_formal','entity','location_name','geo_lat', 'geo_lng', 'class'])
f.close()

location_dictionary = json.load(open('location_dictionary.json'))

def extract_location(text, use_polyglot = False):
	if use_polyglot:
		text = Text(text)
		text.language = 'id'
		locations = [(" ".join(x)).encode('utf-8') for x in text.entities if x.tag == 'I-LOC']
		for loc in locations:
			if loc[0].isupper() and loc.lower() in location_dictionary:
				print 'location: ' + loc
				return (loc, location_dictionary[loc.lower()][0], location_dictionary[loc.lower()][1])
	else:
		print text
		tokens = text.split()
		for token in tokens:
			if token[0].isupper() and token.lower() in location_dictionary:
				print 'location: ' + token
				return (token, location_dictionary[token.lower()][0], location_dictionary[token.lower()][1])
	return ('', 'NULL', 'NULL')

#save tweets
tweets = []
with open(directory + keyword_penyakit + '_labeled.csv', 'r') as f:
	reader = csv.DictReader(f)
	for row in reader:
		if row['class'] == keyword_penyakit:
			if tweets_orig[row['id']]['geo_lat'] == 'NULL' or tweets_orig[row['id']]['geo_lng'] == 'NULL':
				row['location_name'], row['geo_lat'],row['geo_lng'] = extract_location(row['text_original'], use_polyglot=True)
			else:
				row['geo_lat'] = tweets_orig[row['id']]['geo_lat']
				row['geo_lng'] = tweets_orig[row['id']]['geo_lng']
				row['location_name'] = ''

			if not row['geo_lat'] == 'NULL' and not row['geo_lng'] == 'NULL':
	 			tweets.append(row)

	 			f = open(directory + keyword_penyakit + '_geo.csv', 'a')
	 			writer = csv.writer(f)
	 			writer.writerow([row['id'], row['text_original'], row['text_formal'], row['entity'], row['location_name'], row['geo_lat'], row['geo_lng'], row['class']])
	 			f.close()



