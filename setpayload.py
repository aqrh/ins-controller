#!/usr/bin/python3 python3

import json, json_read

def set_payload(username):
	with open('cookies.'+username, 'r') as file:
		cookies_jar = json.load(file)
	cookies = {
		'csrftoken': cookies_jar['csrftoken'],
		'mid': json_read.get_cookies('info')['mid'],
		'ig_did': json_read.get_cookies('info')['ig_did'],
		'ig_nrcb': json_read.get_cookies('info')['ig_nrcb'],
		'ds_user_id': cookies_jar['ds_user_id'],
		'sessionid': cookies_jar['sessionid'],
		#'rur': cookies_jar['rur']
	}

	headers = {
		'Host': "www.instagram.com",
		'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
		'Accept': "*/*",
		'Accept-Language': "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate",
		"X-IG-App-ID": "936619743392459",
		"X-ASBD-ID": "198387",
		"X-IG-WWW-Claim": "0",
		'X-Requested-With': "XMLHttpRequest",
		"Connection": "close",
		"Referer": "https://www.instagram.com/",
		"X-CSRFToken": cookies_jar['csrftoken']
	}
	return headers, cookies