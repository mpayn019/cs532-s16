from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import requests
import json

#Acquired class, main, and some imports from http://adilmoujahid.com/posts/2014/07/twitter-analytics/
access_token = "XXXX"
access_token_secret = "XXXX"
consumer_key = "XXXX"
consumer_secret = "XXXX"

linkList = []
linkDoc = open('./linkList.txt' , 'w+')
class StdOutListener(StreamListener):
    
	def on_data(self, data):
		#Acquired from Catherine Nguyen
		if len(linkList) >= 1000:
			return False
		#/Catherine Nguyen
		json_code = json.loads(data)
		json_code= json_code['user']

		if json.dumps(json_code['url']) != "null":
		#Acquired from Gabriel Marquez
			parsed_code = json.dumps(json_code['url'])
			parsed_code = parsed_code[1:-1]
			status = requests.head("https://www.reddit.com/subreddits/sdfdgfgdf")
			try:
				status = requests.head(parsed_code)
		   
			except requests.exceptions.ConnectionError:
				status.status_code = "derp"
			
			if status.status_code == 200 and parsed_code not in linkList:
				linkList.append(parsed_code)
				linkDoc.write(parsed_code + '\n')
				print parsed_code
		return True
		#/Gabriel Marquez            

	def on_error(self, status):
		pass


if __name__ == '__main__':
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)
	stream.filter(track=['python', 'javascript', 'ruby'])
	linkDoc.close()