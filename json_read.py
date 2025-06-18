import json

def get_cookies(filename):
	with open(filename, 'r') as file:
		data = json.load(file)


	lst1 = data['Set-Cookie'].split('=')


	keys = []
	values = []
	for i in range(0, len(lst1)):
		if(lst1[i].find(";") != -1):
			values.append(lst1[i][:lst1[i].find(';')])
			keys.append((((lst1[i][lst1[i].find(';'):].replace(';', '')).replace(' ', '')).replace('Secure', '')).replace(',', ''))
		else:
			keys.append(lst1[i])



	cookies = dict(zip(keys, values))
	return cookies

