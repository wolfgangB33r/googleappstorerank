"""
Example script for checking the Google App store position 
given an appid and search terms
"""
import requests, time, sched, random, os, ssl

YOUR_DT_API_URL = '???'
YOUR_DT_API_TOKEN = '???'
YOUR_APP_ID = 'at.smartlab.tshop'
KEYWORDS = ['pos', 'point of sale', 'kasse', 'restaurant pos', 'invoice print', 'cashier', 'Cash Register']


def checkAppPosition(appid, searchterm):
	
	HEADERS = {
		"accept-language" : "en-US,en;q=0.9,de;q=0.8", 
		"user-agent" : "Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020c Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Safari/537.36"
	}

	try:
		r = requests.get('https://play.google.com/store/search?q=' + searchterm + '&c=apps', headers=HEADERS)
		seg = r.text.split('JpEzfb')
		c = 1
		for s in seg:
			if s.find(appid) > 0:
				break
			c = c + 1
		return c - 2
	except ssl.SSLError:
		print("SSL Error")


def main():
	metricStr = ""
	for kw in KEYWORDS:
		# if you want to profit from topology in Dynatrace you have to add a link to an entity as dimension: dt.entity.mobile_application=MOBILE-APPLICATION-1234435345
		metricStr += "business.store.rank,store=playstore,appid=" + YOUR_APP_ID + ",searchterm=\"" + kw + "\" " + str(checkAppPosition(YOUR_APP_ID, kw)) + "\n"
	print(metricStr)	
	try:
		r = requests.post(YOUR_DT_API_URL + '/api/v2/metrics/ingest', headers={'Content-Type': 'text/plain', 'Authorization' : 'Api-Token ' + YOUR_DT_API_TOKEN}, data=metricStr)
		print(r.text)
	except ssl.SSLError:
		print("SSL Error")


if __name__ == '__main__':
	main()
