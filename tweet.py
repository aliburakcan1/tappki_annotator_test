import requests
import streamlit.components.v1 as components
import random

class Tweet(object):
	def __init__(self, url, tweet_ids):
		def find_next_tweet(tries=0, url=url):
			try:
				api = "https://publish.twitter.com/oembed?url={}".format(url)
				response = requests.get(api)
				return response.json()['html'], url.split("/")[-1]
			except:
				print("Tweet not found. Trying again.", url)
				if tries < 10:
					tweet_id = random.choice(tweet_ids)
					return find_next_tweet(tries+1, "https://twitter.com/i/status/{}".format(tweet_id))
				else:
					return f"<blockquote class='missing'>This tweet {url} is no longer available.</blockquote>"
		self.text, self.tweet_id = find_next_tweet(0)

	def _repr_html_(self):
		return self.text
	
	def get_tweet_id(self):
		return self.tweet_id

	def component(self):
		return components.html(self.text, height=800, scrolling=True)
	

	