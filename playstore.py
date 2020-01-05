"""
Example script for checking the Google App store position 
given an appid and search terms
"""
import requests, time, sched, random, os, ssl

YOUR_DT_API_URL = '?'
YOUR_DT_API_TOKEN = '?'
YOUR_APP_ID = '?'
KEYWORDS = ['pos', 'point of sale', 'kasse', 'restaurant pos', 'invoice print', 'cashier', 'Cash Register']

def registerDynatraceMetrics():
	tsdef = {
		"displayName" : "Appstore ranking",
		"unit" : "Count",
		"dimensions": ['keyword'],
		"types": [
			"AppStore"
		]
	}

	r = requests.put(YOUR_DT_API_URL + 'api/v1/timeseries/custom:appstore.ranking.perkeyword/?Api-Token=' + YOUR_DT_API_TOKEN, json=tsdef)
	#print(r)


def checkAppPosition(appid, searchterm):
	
	HEADERS = {
		"accept-language" : "en-US,en;q=0.9,de;q=0.8", 
		"user-agent" : "Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020c Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Safari/537.36"
	}

	try:
		r = requests.get('https://play.google.com/store/search?q=' + searchterm + '&c=apps', headers=HEADERS)
		#print("Playstore search: %d" % r.status_code)
		#print(r.text)
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
	registerDynatraceMetrics()

	series = []

	for kw in KEYWORDS:
		series.append({ "timeseriesId" : "custom:appstore.ranking.perkeyword", 
		  "dimensions" : { "keyword" : kw },
		  "dataPoints" : [ [ int(time.time() * 1000)  , checkAppPosition(YOUR_APP_ID, kw) ] ]
		})

	payload = {
     "displayName" : "Google AppStore",  
     "ipAddresses" : [],
     "listenPorts" : [],
     "type" : "AppStore",
     "series" : series
	}

	try:
		print(payload)
		r = requests.post(YOUR_DT_API_URL + 'api/v1/entity/infrastructure/custom/appstore?Api-Token=' + YOUR_DT_API_TOKEN, json=payload)
		print(r)
	except ssl.SSLError:
		print("SSL Error")
	

if __name__ == '__main__':
	main()