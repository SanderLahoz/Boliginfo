import threading
import queue
import requests


def get_proxies():
	url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
	payload = {}
	headers = {"country":"DE", "SSL":"yes", "anonymity":"anonymous", "timeout":"1000"}
	response = requests.request("GET", url, headers=headers, data=payload)

	with open("proxies.txt", "w") as f:
	    f.write(response.text.strip())



q = queue.Queue()
valid_proxies = []

with open("proxies.txt", "r") as f:
	proxies = f.read().split("\n")
	
	while ("" in proxies):
		proxies.remove("")

	for proxy in proxies:
		q.put(proxy)


def check_proxies():
	global q
	while not q.empty():
		proxy = q.get()
		try:
			res = requests.get("https://www.boligsiden.dk/", proxies={"http":proxy, "https:":proxy})
		except:
			continue

		if res.status_code == 200:
			print(proxy)


for _ in range(10):
	threading.Thread(target=check_proxies).start()



