#from google.appengine.api import users
from google.appengine.ext.webapp import template

from models.user import User
from models.word import Word
from models.word_score import WordScore

import datetime
import webapp2

class BoardHandler(webapp2.RequestHandler):
	def get(self):		
		template_params = {}
		
		user = User.checkUser()
		if user:
			template_params['user'] = user.email
			template_params['logoutUrl'] = user.logoutUrl()
		
		template_params['words'] = []
		words = Word.allWords()
		for w in words:
			#we don't want to show today's word in the scoreboard!
			if w.day == datetime.date.today():
				continue
				
			template_params['words'].append({
				"word": w.word,
				"date": w.day
			})
		
		html = template.render("web/templates/scoreboard.html", template_params)
		self.response.write(html)
		
class WordBoardHandler(webapp2.RequestHandler):
	def get(self, word_str):
		template_params = {}
		
		user = User.checkUser()
		if user:
			template_params['user'] = user.email
			template_params['logoutUrl'] = user.logoutUrl()
		
		
		template_params['word_str'] = word_str
		template_params['found'] = True
		word = Word.wordByString(word_str)
		if word is None:
			template_params['found'] = False
		else:
			scores_results = WordScore.scoresForWord(word)
			template_params['scores'] = []
			for score in scores_results:
				u = score.user.get()
				if u is not None:
					template_params['scores'].append({
						"email": "****"+u.email[4:],
						"attempts": score.attempts
					})
				
			
		
		html = template.render("web/templates/wordboard.html", template_params)
		self.response.write(html)

app = webapp2.WSGIApplication([
	('/scoreboard[\/]?', BoardHandler),
	('/scoreboard/(.*)', WordBoardHandler),
], debug=True)
