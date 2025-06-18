#!/usr/bin/python3 python3

import requests, json, select, setpayload
from time import sleep
from datetime import datetime
from sys import exit, stdin, stdout
from termios import tcflush, TCIFLUSH
from os import system

class Controller:
	def __init__(self, *args):
		try:
			self.headers, self.cookies = setpayload.set_payload(args[0])
			self.account = args[0]
			self.username = args[1]
			print(args[0], args[1], self.username, self.account)
			self.link = None
		except Exception as e:
			print("Exception initialize:", e)

	def check_limit(self, x):
		if x >= 90:
			return True
		return False

	def counter(self, count="fol"):
		if count == "unf":
			target = "counteru"
		else:
			target = "counter"

		with open("settings", 'r') as file:
			content = json.load(file)
		content[self.account][target] += 1
		content['day'] = str(datetime.now().day)
		with open("settings", 'w') as file:
			json.dump(content, file)

	def check_reset(self):
		with open("settings", 'r') as file:
			try:
				content = json.load(file)
				return datetime.now().day == int(content['day'])
			except Exception as e:
				print(e)

	def reset_settings(self):
		with open("settings", 'r') as file:
			content = json.load(file)
		content['day'] = datetime.now().day
		for key in content.keys():
			if key == 'day':
				continue
			try:
				content[key]['counter'] = 0
				content[key]['counteru'] = 0
			except:
				continue
		with open("settings", 'w') as file:
			json.dump(content, file)

	def choice(self, time=900):
		print("[*] Sleep", str(time/60) + "m/Enter to skip...")
		a, _b, _c = select.select([stdin], [], [], time)
		if a:
			tcflush(stdin.fileno(), TCIFLUSH)
			return
		return

	def error_handler(self, response):
		print("[!] Status code:", response.status_code)
		try:
			print(response.json())
			json_exist = True
		except:
			print("[!] No json response")
			json_exist = False

		print(datetime.now())
		if response.status_code in [429, 302, 400]:
			if response.status_code == 400:
				print("[!] Bad request: ", response.status_code)
			else:
				print("[!] Too many requests")
			self.choice()
			self.login()
			if json_exist:
				if response.json()['message'] == "checkpoint_required":
					self.take_challenge(self.account)
		elif response.status_code == 401:
			print("[!] Unauthorized...")
			self.choice()
			self.login()
			self.take_challenge(self.account)
		elif response.status_code == 404:
			print(response.status_code)
			sleep(3)
		else:
			print(datetime.now())
			print("[!] Status Code:", response.status_code)
			print("[*] Continue...?")
			input()

	def login(self):
		print("[*] Try logging in...")
		with open("settings", 'r') as file:
			password = json.load(file)[self.account]['password']
		system("python inslogin-2.0.py -u " + self.account + " -p " + password)
		self.headers, self.cookies = setpayload.set_payload(self.account)

	def follow(self, username):
		link = "https://www.instagram.com/api/v1/web/friendships/" + username + "/follow/"
		while True:
			try:
				response = requests.post(link, headers=self.headers, cookies=self.cookies)
				if response.status_code == 200:
					return False
				else:
					print("[*] follow", response)
					self.error_handler(response)
			except Exception as e:
				print("[!] follow:", e)
				sleep(10)
				continue

	def unfollow(self, username):
		link = "https://www.instagram.com/api/v1/web/friendships/" + username + "/unfollow/"
		while True:
			try:
				response = requests.post(link, headers=self.headers, cookies=self.cookies)
				if response.status_code == 200:
					return False
				else:
					print("[*] unfollow")
					self.error_handler(response)
			except Exception as e:
				print("[!] unfollow: ", e)
				sleep(10)
				continue

	def get_followers(self, userid, maxid=0):
		link = f"https://www.instagram.com/api/v1/friendships/{userid}/followers/?count=12&max_id={str(maxid)}"
		lst = {}

		while True:
			try:
				print(link)
				response = requests.get(link, headers=self.headers, cookies=self.cookies)
				if response.status_code == 200:
					for user in response.json()['users']:
						lst[user['username']] = user['id']
					return lst
				else:
					print("[*] get_followers")
					self.error_handler(response)
			except Exception as e:
				print("[!] get_followers:", e)
				sleep(10)
				continue

	def get_followings(self, userid, maxid=0):
		link = f"https://www.instagram.com/api/v1/friendships/{userid}/following/?count=12&max_id={str(maxid)}"
		lst = {}

		while True:
			try:
				response = requests.get(link, headers=self.headers, cookies=self.cookies)
				if response.status_code == 200:
					for user in response.json()['users']:
						lst[user['username']] = user['id']
					return lst
				else:
					print("[*] get_followings")
					self.error_handler(response)
			except Exception as e:
				print("[!] get_followings:", e)
				sleep(10)
				continue

	def getinfo(self, username, demand):
		if not self.link or username not in self.link:
			while True:
				try:
					response = requests.get("https://www.instagram.com/api/v1/users/web_profile_info/?username=" + username, headers=self.headers, cookies=self.cookies)
					if response.status_code == 200:
						self.link = response
						break
					else:
						print("[*] getinfo", response)
						self.error_handler(response)
				except Exception as e:
					print("[!] getinfo:", e)
					sleep(10)
					continue
		if demand == "id":
			return str(self.link.json()['data']['user']['id'])
		elif demand == "is_following":
			if self.link.json()['data']['user']['is_private']:
				return self.link.json()['data']['user']['requested_by_viewer']
			return self.link.json()['data']['user']['followed_by_viewer']
		elif demand == "is_nfb":
			return self.link.json()['data']['user']['follows_viewer']
		else:
			print("[!] getinfo: Demand required!")

	def take_challenge(self, username):
		try:
			response = requests.get("https://www.instagram.com/api/v1/users/web_profile_info/?username=" + self.username, headers=self.headers, cookies=self.cookies)
			response2 = requests.get("https://www.instagram.com/api/v1/challenge/web/?next=" + response.url, headers=self.headers, cookies=self.cookies)
			pars = {"challenge_context": response2.json()["challenge_context"], "has_follow_up_screens": "false", "next_data_manifest": "true"}
			sleep(4)
			response3 = requests.post("https://www.instagram.com/api/v1/bloks/apps/com.instagram.challenge.navigation.take_challenge/", headers=self.headers, cookies=self.cookies, params=pars)
			print(response, response2, response3)
			sleep(5)
			return response3
		except Exception as e:
			print("[!] take_challenge")

	def get_nfb(self, maxid):
		nfb = {}
		while True:
			lst = self.get_followings(self.getinfo(self.account, 'id'), maxid)
			if isinstance(lst, dict):
				print(lst, '\n')
				for user in lst.keys():
					if not self.getinfo(user, "is_nfb"):
						nfb[user] = lst[user]
					sleep(4)
				return nfb
			else:
				print(lst)