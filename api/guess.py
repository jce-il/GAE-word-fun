import webapp2
import json

import config
from models.user import User
from models.word import Word
from models.word_score import WordScore

class GuessHandler(webapp2.RequestHandler):
	def get(self):
		self.post()
		
	def post(self):
		replyJson = {}
		
		user = User.checkUser()
		if not user:
			self.response.set_status(401)
			self.response.write('Need active user to proceed')
			return
		
		guess = self.request.get('word')
		if not guess:
			self.response.set_status(400)
			self.response.write('Can not process an empty guess')
			return
		
		word = Word.todaysWord()
		score = WordScore.getScore(user, word)
		score.incAttempts()
		
		if guess == word.word:
			replyJson['solved'] = True
			replyJson['attempts'] = score.attempts
			score.setSolved()
		else:
			replyJson['solved'] = False
			replyJson['attempts'] = score.attempts
		
		if score.attempts >= config.ATTEMPTS_FOR_CLUE or replyJson['solved']:
			replyJson['wordLen'] = word.len
		
		
		self.response.write(json.dumps(replyJson))

app = webapp2.WSGIApplication([
	('/api/guess', GuessHandler)
], debug=True)