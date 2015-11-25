import csv
import folium

keywords_penyakit = ['dbd', 'diare', 'filariasis', 'ispa', 'malaria']

marker_color = {'dbd':'blue', 'diare':'green', 'filariasis':'red', 'ispa': 'purple', 'malaria':'orange'}

directory = '../dataset/'

#save tweets as dictionary
tweets = []
for keyword_penyakit in keywords_penyakit:
	with open(directory + keyword_penyakit + '/' + keyword_penyakit + '_geo_similarity.csv', 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
	 		tweets.append(row)

map_osm = folium.Map(location=[-2.7088628,117.4906404], zoom_start=5)
 		
for tweet in tweets:
	try:
		if not tweet['location_name'] == '':
			lat = float(tweet['geo_lat'])
			lng = float(tweet['geo_lng'])
			map_osm.simple_marker([lat,lng], popup=tweet['text_original'].replace(tweet['location_name'], "<b>"+tweet['location_name']+"</b>"), marker_color=marker_color[tweet['class']], clustered_marker=True)
	except: 
		continue
map_osm.create_map(path='map.html')

