
import feedparser
import re
import urllib
from bs4 import BeautifulSoup 
from urllib import urlopen
 

# Returns title and dictionary of word counts for an RSS feed
def getwordcounts(url):
  # Parse the feed
  d=feedparser.parse(url)
  wc={}

  # Loop over all the entries
  count = 0
  print(len(d.entries))
  for e in d.entries:
    if 'summary' in e: summary=e.summary
    else: summary=e.description

    # Extract a list of words
    words=getwords(e.title+' '+summary)
    for word in words:
      wc.setdefault(word,0)
      wc[word]+=1
  return d.feed.title,wc

def getwords(html):
  # Remove all the HTML tags
  txt=re.compile(r'<[^>]+>').sub('',html)

  # Split words by all non-alpha characters
  words=re.compile(r'[^A-Z^a-z]+').split(txt)

  # Convert to lowercase
  return [word.lower() for word in words if word!='']


apcount={}
wordcounts={}
filename1 = r'blog.txt'
feedlist=[]
for line in open(filename1):
  feedlist.append(line)
  

for feedurl in feedlist:
  try:
    title,wc=getwordcounts(feedurl)
    wordcounts[title]=wc
    for word,count in wc.items():
      apcount.setdefault(word,0)
      if count>1:
        apcount[word]+=1
  except:
    print('Failed to parse feed %s' % feedurl)
print(len(apcount))

wordlist=[]
#get 500 words in the range
for w,bc in apcount.items():
  frac=float(bc)/len(feedlist)
  if len(wordlist) <= 99:
    #if frac>0.1 and frac<0.9:
    wordlist.append(w)   
print(len(wordlist))

filename2 = r'Raw.txt'
out=open(filename2,'w')
response = urllib.urlopen(feedlist[0])
soup = BeautifulSoup(response, 'html.parser')
out.write(str(soup.encode("utf-8")))