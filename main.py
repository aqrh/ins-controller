import argparse
from time import sleep
from source import Controller
import json
from datetime import datetime
from sys import exit

parser = argparse.ArgumentParser(prog="main.py")
parser.add_argument("account", help="personal account")
parser.add_argument("-u", "--username", help="target username")
parser.add_argument("-f", "--followings", required=False, action="store_true")
parser.add_argument("-flrs", "--followers", required=False, action="store_true")
parser.add_argument("-un", "--unfollow", required=False, action="store_true")
parser.add_argument("-s", "--skip", action='store', type=int, required=False)
args = parser.parse_args()

if not args.followings and not args.followers:
	username = args.account
else:
	if args.followings:
		username = args.followings
	else:
		username = args.followers
print(username)

#check for -u if -f or -flrs is marked
if (args.followings and not args.username) or (args.followers and not args.username):
	print("[!] Need target username with flags -f or -flrs")
	exit()
controller1 = Controller(args.account, username)
try:
	with open("settings", 'r') as file:
		content = json.load(file)
except Exception as e:
	print(e)
maxids = args.skip
if not maxids:
	maxids = 0
list_empty = False

while True:
	with open("exceptions", 'r') as file:
		exceptions = file.read().split('\n')
	if(not controller1.check_reset()):
		print("[*] Reset settings")
		controller1.reset_settings()

	if(controller1.check_limit(int(content[args.account]['counter'])) or controller1.check_limit(int(content[args.account]["counteru"]))):
		print("[!] Limit exceeded...sleep(1h)")
		controller1.choice(3600)
		continue

	if args.followings:
		lst = controller1.get_followings(controller1.getinfo(controller1.username, "id"), maxids)
		print(lst)
		if len(lst) < 1:
			list_empty = True
			maxids = 0
			print("[!] Followings limit reached\n[*] Sleep 2h/Enter...")
			controller1.choice(7200)

	elif args.followers:
		lst = controller1.get_followers(controller1.getinfo(controller1.username, 'id'), maxids)
		print(lst)
		if len(lst) < 1:
			list_empty = True

	elif args.unfollow:
		lst = controller1.get_nfb(maxids)
		print(lst)
	if list_empty:
		args.followings = None
		lst = controller1.get_followings(controller1.getinfo(controller1.username, "id"), maxids)
		print(lst)
		if len(lst) < 1:
			print("[!] list_limit\n[*] Sleep 2h/Enter...")
			controller1.choice(7200)
			list_empty = False
			args.followings = "f"
			maxids = 0

	for user in lst.keys():
		if user in exceptions:
			print("[!]", user, "is an exception")
			continue
		sleep(6)

		while True:
			try:
				if args.followings or args.followers:
					if controller1.getinfo(user, "is_following"):
						print("[!] already following:", user)
						break
					sleep(3)
					status = controller1.follow(lst[user])
					text = "[*] Follow: "
					target = "fol"
				elif args.unfollow or (not args.unfollow and not args.followings):
					if not controller1.getinfo(user, "is_following"):
						print("[!] Not following:", user)
						break
					sleep(4)
					status = controller1.unfollow(lst[user])
					text = "[*] Unfollow: "
					target = "unf"

				if not status:
					print(text + user)
					controller1.counter(target)
				else:
					print(status)
					input("[!] Enter...")
			except Exception as e:
				print(e)
			break

	print(maxids)
	maxids += 12
	print(datetime.now())
	controller1.choice(900)
