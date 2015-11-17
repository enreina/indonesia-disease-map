import json

location_dict = {}
dbpedia_dump = json.load(open('id-dbpedia.dump'))
for data in dbpedia_dump['results']['bindings']:
	names = data['name']['value'].lower()
	names = names.split(",")
	for name in names:
		if name.strip() not in location_dict:
			location_dict[name.strip()] = (data['lat']['value'], data['long']['value'])

	aliases = data['aliasLabel']['value'].lower()
	aliases = aliases.split(",")
	for alias in aliases:
		if alias.strip() not in location_dict:
			location_dict[alias.strip()] = (data['lat']['value'], data['long']['value'])

json.dump(location_dict, open('location_dictionary.json', 'w'))