import json

x = "football"

with open('sport_url_data.json') as json_file:
	data = json.load(json_file)

	unique_pos = data[x]['sport_root_url']
	print(unique_pos)
	print(list(data.keys()))
	print(data[x]["url"])
	print("Type:", type(data))




# a = {
# 	'basketball': {
# 		'site_name': 'Basketball-reference.com', 
# 		'url': 'https://www.basketball-reference.com/leagues/NBA_', 
# 		'root_url': 'https://www.basketball-reference.com/'
# 	}, 
# 	'football': {
# 		'site_name': 'pro-football-reference.com', 
# 		'url': 'https://www.pro-football-reference.com/years/', 
# 		'root_url': 'https://www.pro-football-reference.com/'
# 	}
# }

# b = {
# 	'site_name': 'a',
# 	'url': 'b',
# }

# print(a)
# print()
# print(b)