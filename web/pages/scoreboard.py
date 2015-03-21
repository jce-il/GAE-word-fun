#from google.appengine.api import users
from google.appengine.ext.webapp import template

from models.user import User
from models.word import Word
from models.word_score import WordScore
import webapp2

class BoardHandler(webapp2.RequestHandler):
	def get(self):		
		template_params = {}
		user = User.checkUser()
		if not user:
			template_params['loginUrl'] = User.loginUrl()
		else:
			template_params['logoutUrl'] = User.logoutUrl()
			template_params['user'] = user.email
			
		html = template.render("web/templates/scoreboard.html", template_params)
		self.response.write(html)
		
class WordBoardHandler(webapp2.RequestHandler):
	def get(self, word):		
		template_params = {"word":word}
		user = User.checkUser()
		if not user:
			template_params['loginUrl'] = User.loginUrl()
		else:
			template_params['logoutUrl'] = User.logoutUrl()
			template_params['user'] = user.email
			
		html = template.render("web/templates/wordboard.html", template_params)
		self.response.write(html)

app = webapp2.WSGIApplication([
	('/scoreboard[\/]?', BoardHandler),
	('/scoreboard/(.*)', WordBoardHandler),
], debug=True)
