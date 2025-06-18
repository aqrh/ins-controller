#!/usr/bin/python3 python3

import argparse
import requests
from datetime import datetime
import json
import json_read
from os import system

time = int(datetime.now().timestamp())

parser = argparse.ArgumentParser(prog="inslogin-2.0.py", description="Login credentials")
parser.add_argument('-u', '--username', action='store', type=str, required=True, help="Instagram username")
parser.add_argument('-p', '--password', action='store', type=str, required=True, help="account password")

args = parser.parse_args()

headers={
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
	"Referer": "https://www.instagram.com/"
}

response = requests.get("https://www.instagram.com/api/v1/public/landing_info/", headers=headers)


with open("info", 'w') as file:
	json.dump(dict(response.headers), file)

cookies = json_read.get_cookies("info")

headers['X-CSRFToken'] = cookies['csrftoken']
link = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
payload = {
	'enc_password': f"#PWD_INSTAGRAM_BROWSER:0:{time}:{args.password}",
	'username': args.username,
	'queryParams': {},
	'optionOneTap': "false",
	'trustedDeviceRecords': {}
}

login_cookies = {
	'csrftoken': cookies['csrftoken'],
	'mid': cookies['mid'],
	'ig_did': cookies['ig_did'],
	'ig_nrcb': cookies['ig_nrcb']
}

response = requests.post(link, headers=headers, cookies=login_cookies, data=payload)

if(response.json()['status'] == 'ok' and response.json()['authenticated'] == True):
	cookies_jar = response.cookies.get_dict()
	print(response.status_code)
	print(response.json())
	print(cookies_jar)
	with open('cookies.'+args.username, 'w') as file:
		json.dump(cookies_jar, file)
	print('[!] Login success')
else:
	print("[!] Login failed!")
	print(response)
	print(response.json())

system("rm info")