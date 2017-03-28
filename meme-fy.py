import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import sys
import json
import unicodedata
import re

consumer_key = 'Ll9MmBt6gz0il5dVIAlMDzXNK'
consumer_secret = 'fp16yxan6ShPD5FMoZmQ9tBvCQkFJUiPpTyETGs4EBejnFVenm'
access_token = '4644448902-Fyyc5weYHNp7Jw8hS1MosQI4QA3rvWTmkLmLR40'
access_secret = 'ElG9v2RK61yQUo4ILqwudYi9YeyPA7lwXaNLSYegUW8ua'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
class MyListener(StreamListener):
	def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
		enc = file.encoding
		if enc == 'UTF-8':
			print(*objects, sep=sep, end=end, file=file)
		else:
			f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
			print (*map(f, objects), sep=sep, end=end, file=file)
		print(*map(f, objects))

	def on_data(self, data):	
		json_text = json.loads(data)
		text = json_text['text']
		print("retweet_count: "+str(json_text['retweet_count']))
		print("favorite_count: "+str(json_text['favorite_count']))
		text = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
		text = re.findall(r'(https?://[^\s]+)', str(text))
		self.uprint(text)
		if json_text['retweet_count'] > 0 or json_text['favorite_count'] > 0:
			try:
				with open('urls.txt', 'a') as f:
					for each in text:
						f.write(each+"\n")
					return True
			except BaseException as e:
				print('Error on_data: ' +str(e))
			return True
 
	def on_error(self, status):
		#print(status)
		return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#funny'])
