#from google.appengine.api import users
import config
import logging

from google.appengine.ext.webapp import template

from models.user import User
from models.word import Word
from models.word_score import WordScore
import webapp2

class IndexHandler(webapp2.RequestHandler):
	def get(self):
		template_params = {}
		user = User.checkUser()
		
		if not user:
			self.redirect('/')
			return
		
		template_params['user'] = user.email
		template_params['logoutUrl'] = user.logoutUrl()
		
		word = Word.todaysWord()
		score = WordScore.getScore(user, word)
		logging.info("--------- Wrd score: Word: {}, Solved: {}".format(word.word, score.solved))
		template_params['definition'] = word.definition
		if score.attempts >= config.ATTEMPTS_FOR_CLUE:
			template_params['wordLen'] = word.len
		
		
		template_params['solved'] = score.solved
		template_params['attempts'] = score.attempts
		
		html = template.render("web/templates/game.html", template_params)
		self.response.write(html)

app = webapp2.WSGIApplication([
	('/game', IndexHandler)
], debug=True)
