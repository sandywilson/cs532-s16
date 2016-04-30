import json
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import re
import urllib.request
from bs4 import BeautifulSoup 
import os

access_token = "4856503619-3DtfcYGPx95jS5FuL7WX6tpr1sTQ1b1Kmx5cQiL"
access_token_secret = "9tHO78XZxo9rGwJB9D3ox8MPXGLzHNpZmOk9ZmsniQPWg"
consumer_key = "lYUHPYN8uCL84oesFXnhH9FSh"
consumer_secret = "wCPmeGp2s5v0mLq3c56aa5PjJMzpV2YxNhy2XAPRuUsMNPrS6X"

auth = twitter.oauth.OAuth(atoken, asecret,
                           ckey, csecret)

twitter_api = twitter.Twitter(auth=auth)

count = 10000
statuses = twitter_api.statuses.home_timeline(count = 10000)

print("length: ", len(statuses))

# Show one sample search result by slicing the list...
#print(json.dumps(statuses[0], indent=1))

# get url data into lists
url_links = [ user_mention['expanded_url'] 
                 for status in statuses 
                     for user_mention in status['entities']['urls'] ]

#makes sure link is only in list once
list = []
listcount = 0
for links in url_links:
	if links in list:
		pass
	else:
		list.append(links)

#Unique list of links
for links in list:
	#print("Linkes are: ", links)
	listcount = listcount + 1
print("List is: ", listcount)
newlist = []
for link in list:
	newlist.append(link)
temp = 0
value = 0
while temp == 0:
	if len(newlist) <= 1000:
		while value < len(list):
			print("Index:", value)
			print("Old List:", len(list))
			try:
				response = urllib.request.urlopen(list[value])
				soup = BeautifulSoup(response, 'html.parser')
				for temp in soup.find_all('a'):
					try:
						response1 = urllib.request.urlopen(temp.get('href'))
						if temp.get('href') in newlist:
							pass
						else:
							if len(newlist) == 1000:
								temp = 1
								value = len(list) + 1
							else:
								newlist.append(temp.get('href'))
								print("New List is: ", len(newlist))
					except:
						pass
				value = value + 1
				print("Value", value)
			except:
				value = value + 1
				pass
	else:
		temp = 1
print("New List is: ", len(newlist))
print("Done", len(newlist))
filename = "output.txt"
outfile = open(filename, 'w')
outfile.write("\n".join(newlist))
outfile.close()