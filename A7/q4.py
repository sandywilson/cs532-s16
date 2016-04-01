import math
from math import *
import scipy
from scipy import stats
from scipy.spatial import distance

def get_prefs(dataList,itemList,userList):
    '''Create a dictionary of people and the movies that they have rated. 
    '''
    # This code taken from page 26 in collective intelligence book

    movies = {}
    for movie in itemList:
        movie_id = movie['movie_id'] 
        movie_title = movie['movie_title']
        movies[movie_id] = movie_title

    prefs = {}

    for dataPoint in dataList:
        user_id = int(dataPoint['user_id'])
        movieId = dataPoint['item_id']
        rating = dataPoint['rating']
        prefs.setdefault(user_id,{})
        prefs[user_id][movies[movieId]] = float(rating)
    return prefs

correlation={}
def recommandate(pid):
	correlation={}
	pickedMovie=linktable[pid]
	for mid in linktable :
		if mid==pid:
			continue
		pickedMovieRating=[]
		currentMovieRating=[]
		for uid in pickedMovie:
			if  uid in linktable[mid] :
				pickedMovieRating.append(pickedMovie[uid])
				currentMovieRating.append(linktable[mid][uid])
		if len(currentMovieRating)==0 :
			correlation[mid]=0
		else:
			correlation[mid]=scipy.stats.pearsonr(pickedMovieRating,currentMovieRating)[0]
			if not correlation[mid] or math.isnan(correlation[mid]) :
				correlation[mid]=float(1)/(float(1)+scipy.spatial.distance.euclidean(pickedMovieRating,currentMovieRating))
	correlationArray=sorted(correlation,key=correlation.get,reverse=True)
	print('Top 5 most correlated movies:')
	for m in  correlationArray[:5] :
		print(movies[m] +'  ( correlation: '+str(correlation[m])+' ) ')

	print('Bottom 5 least correlated movies:')
	for m in correlationArray[-5:] :
		print(movies[m]+' ( correlation: '+str(correlation[m])+' ) ')

#parse rating file
linkfile=open('data_files/u.data')
strline=linkfile.readlines()
for line in strline:
	uid,itemid,rating,_=line.split('\t')
	if itemid not in linktable:
		linktable[itemid]={}
	linktable[itemid][uid]=float(rating)
linkfile.close()
#parse movie file
moviefile=open('data_files/u.item')
strline=moviefile.readlines()
for line in strline:
	tuples=line.split('|')
	movies[tuples[0]]=tuples[1]
moviefile.close()

#calculate correlation
pickedId='12'
print('Most favorite movie: 12|Usual Suspects, The (1995)|14-Aug-1995|')
recommandate(pickedId)
print
print('Least favorite movie: 1680|Sliding Doors (1998)|01-Jan-1998|')
pickedId='870'
recommandate(pickedId)