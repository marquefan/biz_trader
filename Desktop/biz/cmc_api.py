#coding=utf-8
import urllib2, json

def fetch_price(coin_name):
	url = "https://api.coinmarketcap.com/v1/ticker/" + str(coin_name)
	ua = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0"
	head = {'User-agent': ua}

	try:
		request = urllib2.Request(url, None, head)
		response = urllib2.urlopen(request).read()

		jsonresponse = json.loads(response)

		return jsonresponse[0]["price_btc"]
	except: 
		print "couldnt find coin on coinmarketcap: ",coin_name