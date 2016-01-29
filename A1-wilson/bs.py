from bs4 import BeautifulSoup	#used to declare the location of the library and to import it
import requests 		#used to import the requests library to be used for declaring the urls
import urllib2			#The main library used

url = raw_input("URL Please: ")	#To allow the user to imput their own URL
response = requests.get(url)	#Setting response to be the name of the urls

page = str(BeautifulSoup(response.content, 'html.parser'))	#used to read the html file and to access BS4


def urlextractor(page):		#definiton for the website being parsed
    start_link = page.find('href')	#the inital link used to find links inside the page
    if start_link == -1:		#If there is no links then no URI's exist
        return None, 0
    start_quote = page.find('"', start_link)	#starts the url extraction process
    end_quote = page.find('"', start_quote + 1) #
    url = page[start_quote + 1: end_quote]
    return url, end_quote

while True:	#the loop to determine if a url will be produced
    url, n = urlextractor(page)
    page = page[n:]
    if url:		#if it exisits print if not then go back to the begging until
        print url	#there are no more start links
    else:
        break