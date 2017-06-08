#! usr/bin/python
# coding=utf-8
from BeautifulSoup import BeautifulSoup
import urllib2, json, datetime, time, os

"""

 statt tägliches update --> stündlich --> 4chan api    time (in milliseconds?)

"""

def main():
	url = "http://api.4chan.org/biz/catalog.json"
	# Beispiel Header --> sonst 403 keine permission
	ua = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0"
	head = {'User-agent': ua}
	request = urllib2.Request(url, None, head)
	response = urllib2.urlopen(request).read()

	jsonresponse = json.loads(response)

	data = []
	count = 0
	pagecount = 0

	for page in jsonresponse:
		count += 1
		threadcount = 0			# Page -> Thread -> Post
		for thread in page["threads"]:
			print "Thread", threadcount
			threadcount+=1
			num = thread["no"]		#Nummer/ID vom thread
			try:
				tmpurl = 'http://api.4chan.org/biz/res/' + str(num) + '.json'
				req = urllib2.Request(tmpurl, None, head)
				replies = urllib2.urlopen(req).read()
			except:
				print "Thread 404 'd"
				break
			time.sleep(0.0001) 	#4chan API Regel? - scheiß drauf
			jsonreplies = json.loads(replies)

			for post in jsonreplies["posts"]:
				try:		
					data.append(BeautifulSoup(str(post["com"])))
				except:
					print "wrong here: ",post 	#manche failen --> evt fehlende informationen
					break
	soup_data = convert_html_to_textlist(data)	
	data_string = "\n".join(soup_data)

	write_file(data_string)

def convert_html_to_textlist(list):
	convertedList = []
	for element in list:		#einzelne Einträge in BS formatieren, überflüssig?
		convertedList.append(BeautifulSoup(str(element)).getText())
	return convertedList

def write_file(content):
	try:
		filename = "data/biz-info-" + str(datetime.date.today()) + ".txt"
		#if os.path.exists(filename):
		#	print "--",filname,"-- already exists"	
		#else:
		file = open(filename, "w+")
		file.write(content)
		file.close()
	except:
		print "Error occured while writing to/a File!"

if __name__ == "__main__":
	main()
