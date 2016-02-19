from StringIO import StringIO

import pycurl
import requests
import certifi
import lynx
import re
from bs4 import BeautifulSoup

i = 0
for line in open('1k.txt','r'):				
    docnumber = './doc' + str(i) + '.txt'
    prodocnumber = './prodoc' + str(i) + '.txt'		#name to open doccument
    docs = open(docnumber , 'w+')
    prodocs = open(prodocnumber , 'w+')
    							
    url = str(line)
    url = url[:-1]       				#To aquire urls
    storage = StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.CAINFO, certifi.where())
    c.setopt(c.URL, url)				#Curl uri to file
    c.setopt(c.WRITEFUNCTION, storage.write)
    c.perform()
    c.close()
    content = storage.getvalue()
    docs.write(content)
    

    Html = docs.read()
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr,'', Html)
    print cleantext
    prodocs.write(cleantext)
    							
    docs.close()					#close the doccuments and ++ to the i
    prodocs.close()
    print line
    i = i + 1
