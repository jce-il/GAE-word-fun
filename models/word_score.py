#this model keeps the score per word per user


from google.appengine.ext import ndb

from user import User
from word import Word

class WordScore(ndb.Model):
	word = ndb.KeyProperty(kind=Word)
	user = ndb.KeyProperty(kind=User)
	attempts = ndb.IntegerProperty(default=0)
	solved = ndb.BooleanProperty(default=False)
	
	@staticmethod
	def getScore(user, word):
		score = WordScore.query(WordScore.user == user.key, WordScore.word == word.key).get()
		if score is None:
			score = WordScore()
			score.user = user.key
			score.word = word.key
			score.put()
			
		return score
	
	def incAttempts(self):
		self.attempts += 1
		self.put()
		return self.attempts
	
	def setSolved(self):
		self.solved = True
		self.put()
		