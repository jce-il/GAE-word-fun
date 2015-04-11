"""
this model represents the daily word
it fetches the word from the remote api if it is not yet in the database
otherwise fetches from db
"""

import sys
sys.path.insert(0, 'lib')	#we need these two lines in order to make libraries imported from lib folder work properly

import datetime
import requests
from google.appengine.ext import ndb

API_KEY = 'a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5'	#word of the day api key
URL_PATTERN = 'http://api.wordnik.com:80/v4/words.json/wordOfTheDay?date={0}-{1:02d}-{2:02d}&api_key={3}'


class Word(ndb.Model):
	word = ndb.StringProperty()
	day = ndb.DateProperty(auto_now_add=True)
	definition = ndb.TextProperty()
	len = ndb.ComputedProperty(lambda self: len(self.word))		#creates a field from the word length automatically
	
	@staticmethod
	def allWords():
		return Word.query()
	
	#returns a word matching the string passed, None is word doesnt exist
	@staticmethod
	def wordByString(str):
		word = Word.query(Word.word == str).get()
		return word
		
	"""
	This function gets the word of the day from the databse, or gets one from the api if no word for today was found
	api docs: http://developer.wordnik.com/docs.html#!/words/getWordOfTheDay_get_1
	"""
	@staticmethod
	def todaysWord():
		today = datetime.date.today()
		word = Word.query(Word.day == today).get()	#try to fetch today's word from db
		if word is None:	#if not found, we fetch from the api
			requestURL = URL_PATTERN.format(today.year, today.month, today.day, API_KEY)
			reply = requests.get(requestURL).json()
			word = Word()
			word.word = reply['word']
			word.definition = reply['definitions'][0]['text']
			word.put()
			
		return word
			