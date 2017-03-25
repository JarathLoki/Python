#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import requests
import re
import time

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

def file_dl(url):
	#Using requests on a for loop of all URLS in the array
	local_filename = str(datetime.now("%a, %d %b %Y %H:%M:%S") + url.split(' -')) #output should be "Sat, 25 Mar 2017 H:M:S -https://blah.com/blah"
	r = requests.get(url, Stream = True) #Must enable stream for full download

	with open(local_filename, 'wb') as file:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk: #always True until file completes
				file.write(chunk)
	return local_filename

def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=5)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	'''
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))
	'''
	#transform the tweepy tweets into a 2D array that will populate the csv	
	#outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	collectedtweets = [[tweet.text.encode("utf-8")] for tweet in alltweets]
	
	'''START OF MY EDITS'''
        #urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(outtweets))
        urls = [re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-&(-_@.&+])+', str(collectedtweets))]
        for url in urls:
        	file_dl(urls)
        	time.sleep(25)
        '''use this for visible output of urls''' 
        #print(urls)
        #print str(outtweets)
	
	
	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("checkmydump")