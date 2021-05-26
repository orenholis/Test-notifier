import json


def load_json_value(value_name):
	f = open('config.json', "r")
	data = json.loads(f.read())
	token = data[value_name]
	f.close()
	return token
