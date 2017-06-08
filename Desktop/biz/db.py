# coding=utf-8
from tinydb import TinyDB, Query
import json
db = TinyDB("./db/db.json")
Coin = Query()


def create_db(data):
	db.insert(
		{
			"coin" 			:		data["coin"],
			"value" 		: 		data["value"], 
			"timestamps" 	:  		[data["timestamp"]],
			"time_updates"	:		"cooming soon",
			"price_history" : 		[]
		}
	)

def get_id(target):
	Coin = Query()
	try:
		id = db.get(Coin.coin == target).eid
		return id
	except:
		print "couldnt fetch id from: ",target

def get_val(target_id, key):
	#coinID = get_id(target)

	val = db.get(eid=target_id)[key]
	return val

def update_db(target, value):
	target_id = get_id(target)
	values = get_val(target_id, value)
	values.append(value)
	
	db.update({"value" : values}, eids=[get_coin])
	print values

def update_multiple(targets, values, timestamps):
	Coin = Query() 
	for i, coin in enumerate(targets):
		#id = db.get(Coin.coin == coin[0]).eid
		id = get_id(coin[0])

		valuesOfOneCoin = get_val(id, "value")
		valuesOfOneCoin.append(values[i])

		timeStampOfOneCoin = get_val(id, "timestamps")
		print timeStampOfOneCoin
		timeStampOfOneCoin.append(timestamps[i])

		db.update({"value" : valuesOfOneCoin, "timestamps":timeStampOfOneCoin}, eids=[id])
	print values

def calc_average(coins):
	for coin in coins:
		id = get_id(coin[0])
		mentions = get_val(id, "value")
		sum = 0
		length = 0
		for val in mentions:
			length += 1
			sum += val
		avgr = sum/length
		db.update({"average" : avgr}, eids=[id])

def get_timestamps(coin):
	id = get_id(coin)

	timestamps = db.get(eid=id)["timestamps"]
	
	return timestamps
	#db.update({"value" : target}, Coin.va)

def init_db(currencylist, coincounter, coin_dates, price):
	try:
		test = get_timestamps("bitcoin")	#wenn die funktion einen fehler zurück gibt -> kein datum vorhanden
	except:
		for index, currency in enumerate(currencylist):				
			create_db(
				{
					"coin" : currency[0],
					"value" : [coincounter[index]],
					"average_mentions" : [coincounter[index]],
					"timestamp" : str(coin_dates[index]),
					"update_timestamp" : "coming soon",
					"price_history" : price
				}
			)
		print "CREATED DB!"