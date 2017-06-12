# coding=utf-8
import sys, re, optparse, datetime, time, glob, os
from HTMLParser import HTMLParser
from db import *
from cmc_api import *
# USAGE
# 	python analyze_content.py info.txt

# !! implement fetch_price

# FLAGS
parser = optparse.OptionParser()

parser.add_option("--ncoins", dest="howmanybestcoins", help="How many of the best coins do you want?")
(options, args) = parser.parse_args()

howmanybestcoins = int(options.howmanybestcoins)

def main():
	starting_time = time.time()
	content = ""
	try: 
		content = get_list_from_file("data/"+sys.argv[3]).lower()
		print "analyze data from: ",sys.argv[3]
	except:
		file_list = glob.glob("data/*")
		content = get_list_from_file(max(file_list, key=os.path.getctime))   # letzte Datei finden
	#real list: compare/coins.txt
	currencylist = get_list_from_file("compare/coins.txt").lower()
	currencylist = currencylist.split("\n")
	coincounter = [0] * len(currencylist)
	coin_dates = [None] * len(currencylist)
	coin_prices = [0] * len(currencylist)
	# verschiedene bezeichnungen für die coins aufsplitten -> 2d Array
	for currency_index, coin in enumerate(currencylist):
		currencylist[currency_index] = coin.split(",")

	counter = 0
	content = content.split("\n")

	for index, post in enumerate(content): 
		htmlparser = HTMLParser()
		content[index] = htmlparser.unescape(content[index])
	
		for coinindex, currency in enumerate(currencylist):
			for currency_name in currency:
				if contains_word(currency_name)(content[index].replace("/", " ")):
					#.replace damit eth/btc gefunden werden kann
					coincounter[coinindex] += 1
					#print currency_name, "was found, +1 ->",coinindex
					coin_dates[coinindex] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
			
	init_db(currencylist, coincounter, coin_dates, coin_prices)
	calc_average(currencylist)
	delta_time = time_delta()
	if delta_time >= 30:
		update_multiple(currencylist, coincounter, coin_dates)

		print "UPDATED DB"
	else:
		print "Too short time interval for update, time_delta(min. 30 MIN): ",delta_time
		#content[index] = re.sub("\W+", " ", post)	# Sonderzeichen loswerden
		

	if options.howmanybestcoins:
		get_best_coin(currencylist, coincounter, howmanybestcoins)
	print "took:",time.time()-starting_time, "s"
	
def get_best_coin(currencylist, coincounter, howmany):
	bestcoins = [[x for x in range(2)] for y in range(howmany)]
	bestcoin_names = [None] * howmany

	for index, coin in enumerate(coincounter):
		for i in range(howmany):
			if coin > bestcoins[i][0]:
				bestcoins[i][0] = coin 	# coin-wert (erwähnungen)
				bestcoins[i][1] = currencylist[index][0]  #tatsächlicher name
				break
		bestcoins.sort()  # sortieren damit nicht nur erste ersetzt wird
	print "best coins are: \n"
	print bestcoins, "\n"

def contains_word(w):
	return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def time_delta():
	# !! wenn in der DB ein Timestamp 'None' ist --> Fehler
	date_now = date_to_integer(datetime.datetime.now())
	last_date = date_to_integer(datetime.datetime.strptime(get_timestamps("bitcoin")[-1], "%Y-%m-%d %H:%M"))
	delta = date_now - last_date 

	return delta

def get_list_from_file(filename):
	#try:
	file = open(filename, "r")
	content = file.read()
	file.close()
	return content
	#except:
	#	print "Error while opening ",filename


def date_to_integer(dt_time):
    return 10000*dt_time.day + 100*dt_time.hour + dt_time.minute


if __name__ == "__main__":
	main()