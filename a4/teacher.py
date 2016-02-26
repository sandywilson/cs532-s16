# -*- code: utf-8 -*-
import xml.etree.ElementTree as ET
import sys 
from xml.dom import minidom
import json

# Extracts a node and all of it's attributes
def extractFriend(friendNode):
	Friend = {}
	elements = friendNode.getElementsByTagName('data')
	
	for element in elements:
		Friend[element.attributes['key'].value] = element.firstChild.data
	return Friend


# Extracts data on all of the friends
def extract_friend_data(inputFileName):
	friendList = {}
	xmldoc = minidom.parse(inputFileName)
	friendNodes = xmldoc.getElementsByTagName('node')

	for friend in friendNodes:
		friend_data = extractFriend(friend)
		friendList[friend.getAttribute('id')] = friend_data


	print(json.dumps(friendList,indent=4))
	return friendList

def create_plot_data(friendData):
	sortedArray = []
	output = []
	output = open('extracredit.txt','w')
	#outputArray.append("id,number_of_friends,name\n")
	counter = 0
	for friendKey in friendData.keys():
		if friendData[friendKey].has_key(u'friend_count'):
			#toPrint = str(counter) +',' + str(friendData[friendKey][u'friend_count']) + "," + str(friendData[friendKey]['name']) +'\n'
			#outputArray.append(toPrint)
			sortedArray.append([int(friendData[friendKey][u'friend_count']),str(friendData[friendKey]['name'])])
			#counter +=1
	sortedArray.append([len(friendData),'Michael Nelson'])

	v = sorted(sortedArray,key=lambda x:x[0])
	output.write("id,number_of_friends,name\n")
	for line in v:
		toPrint = str(counter) + ',' + str(line[0]) + ',' + line[1] + '\n'
		output.write(toPrint)
		counter += 1
	output.close()

if __name__=='__main__':
	fileName = None
	if len(sys.argv) != 2:
		fileName = 'mln.graphml'
	else:
		fileName = str(sys.argv[1])


	data = extract_friend_data(fileName)
	create_plot_data(data)