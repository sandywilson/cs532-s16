from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import time
import json
#removed
# obtained http://pythoncentral.io/introduction-to-tweepy-twitter-for-python/
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	ids = []
	frndList = {}

	if(api.verify_credentials):
		print("Credentials - Verified")
		print("Aquiring followers")
		user = tweepy.Cursor(api.followers,screen_name="phonedude_mln").items()
		while True:
			try:
				u = next(user)
				frndList[u.screen_name] = {'number_of_followers':0}
			except:
				print("Please wait.....................")
				with open('twitter_followers.json','w') as f:
					json.dump(frndList,f)
				time.sleep(15*60)
				
				u = next(user)
				frndList[u.screen_name] = {'number_of_followers':0}

		with open('twitter_followers.json','w') as f:
			json.dump(frndList,f)

	v = open('twitter_followers.json','r')
	frndList = json.loads(v.readline())
	for key in frndList.keys():
		print(key)
	
	follower_dict = {}
	v = 2