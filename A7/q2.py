from data_extractor import read_data_files

import argparse 
import logging
import threading  
import sys
import os
import math 



logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',datefmt='%m-%d %H:%M:%S',filename='correlation.log',filemode='w')

defaultLogger = logging.getLogger('default')


def get_prefs(dataList,itemList,userList):
	'''Create a dictionary of people and the movies that they have rated. 
	'''
	# This code taken from page 26 in collective intelligence book

	movies = {}
	for movie in itemList:
		movie_id = int(movie['movie_id'])
		movie_title = movie['movie_title']
		movies[movie_id] = movie_title

	prefs = {}

	for dataPoint in dataList:
		user_id = int(dataPoint['user_id'])
		movieId = int(dataPoint['item_id'])
		rating = dataPoint['rating']
		prefs.setdefault(user_id,{})
		prefs[user_id][int(movieId)] = float(rating)
	return prefs


def sim_pearson(prefs,p1,p2):
	#This code taken from page 13 in collective intelligence book

	similarItems={}

	for item in prefs[p1]:
		if item in prefs[p2]:
			similarItems[item] = 1

	# Find the number of elements 
	n = len(similarItems)

	# If they have no items in common return 0
	if n == 0:
		return 0

	# Add up all the preferences 
	sum1 = sum([prefs[p1][it] for it in similarItems])
	sum2 = sum([prefs[p2][it] for it in similarItems])

	# Sum up the squares 
	sum1Sq = sum([math.pow(prefs[p1][it],2) for it in similarItems])
	sum2Sq = sum([math.pow(prefs[p2][it],2) for it in similarItems])

	# Sum up the products 
	pSum = sum([prefs[p1][it] * prefs[p2][it] for it in similarItems])

	# Calculate the pearson score 
	num = pSum - (sum1*sum2/n)

	den = math.sqrt((sum1Sq-pow(sum1,2)/n) * (sum2Sq-pow(sum2,2)/n))
	
	# Check if the denominator is zero
	if den == 0:
		return 0
	
	r = num/den

	return r


def user_correlation(userId,dataList,userList,itemList,result,pref_list): 
	# Compute the correllation for the userIds. 
	# Comes from slide 40, week-10-ci-recomender, Calculating pearson's r
	# Code came from: http://stackoverflow.com/questions/16063839/scipy-pearsons-correlation-returning-always-1
	# Uses function: http://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.stats.pearsonr.html

	correlationCoefficients = []
	for user in userList:
		correlationCoefficients.append({'user_id':user['user_id'],'correlation_coefficent':sim_pearson(pref_list,userId,user['user_id'])})
	result[userId] = sorted(correlationCoefficients,key=lambda x: x['correlation_coefficent'],reverse=True)
	


def printResults(userId,correlationCoefficents):
	topFiveMostCorrelated = correlationCoefficents[:6]
	topFiveLeastCorrelated = correlationCoefficents[len(correlationCoefficents) - 6:]

	heading1 = 'Results for: {userId}'.format(userId=userId)
	print('{heading:-^54}'.format(heading=heading1))

	# Print heading for top 5 
	print('{heading:-^54}'.format(heading='Top Five Most Correlated'))

	for i in range(len(topFiveMostCorrelated)):
		print('{rank}){uid:.<48}{correlation_coeffient:<+6}'.format(rank=i+1,uid=topFiveMostCorrelated[i]['user_id'],correlation_coeffient=topFiveMostCorrelated[i]['correlation_coefficent']))

	# Print least correlated 
	print('{heading:-^54}'.format(heading='Top Five Least Correlated'))
	for i in range(len(topFiveMostCorrelated)):
		print('{rank}){uid:.<48}{correlation_coeffient:<+6}'.format(rank=i+1,uid=topFiveLeastCorrelated[i]['user_id'],correlation_coeffient=topFiveLeastCorrelated[i]['correlation_coefficent']))
	print(54*'-')
	print(54*'-')


	#pass

if __name__ == '__main__':
	dataList,userList,itemList = read_data_files(dataName='data_files/u.data',itemName='data_files/u.item',userName='data_files/u.user')
	prefs = get_prefs(dataList,itemList,userList)
	arguments = list(sys.argv)

	userThreads = [] # A list of user threads. 
	userThreadResults = {} # A list of results from those threads
	
	# Check for help flag 
	if '-h' in arguments:
		print("Usage: <user-id-num>...")
	else:
		for userId in range(1,len(sys.argv)):
			# Check to see if the userId is valid 
			if len(list(filter(lambda user: user['user_id'] == int(sys.argv[userId]),userList))) != 0:
				defaultLogger.debug("Creating thread for: {user_id}".format(user_id=sys.argv[userId]))
				# Create thread to process the user if the id is valid 
				userThreads.append(threading.Thread(name=str(sys.argv[userId]),target=user_correlation,args=(int(sys.argv[userId]),dataList,userList,itemList,userThreadResults,prefs)))
			else:
				defaultLogger.error("{user_id} not valid".format(user_id=sys.argv[userId]))

		if len(userThreads) != 0:
			defaultLogger.info("Computing Correlation for {0} userIds".format(len(userThreads)))
			for thread in userThreads:
				thread.start()
				defaultLogger.info("Thread: {threadId} started.".format(threadId=thread.getName()))


			# Wait for all of the threads to terminate 
			defaultLogger.info("Waiting for {numThreads} threads to complete".format(numThreads=len(userThreads)))
			while True:
				if len(filter(lambda t: t.is_alive(),userThreads)) == 0:
					break

			defaultLogger.info("{numThreads} threads completed".format(numThreads=len(userThreads)))

			for result in userThreadResults.keys():
				printResults(result,userThreadResults[result])

		else:
			defaultLogger.info("No user ids to process.")


