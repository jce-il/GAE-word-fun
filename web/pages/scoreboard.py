#from google.appengine.api import users
from google.appengine.ext.webapp import template

from models.user import User
from models.word import Word
from models.word_score import WordScore
import webapp2

class BoardHandler(webapp2.RequestHandler):
	def get(self):		
		template_params = {}
		
		html = template.render("web/templates/scoreboard.html", template_params)
		self.response.write('whole board')
		
class WordBoardHandler(webapp2.RequestHandler):
	def get(self, word):		
		template_params = {}
		
		html = template.render("web/templates/wordboard.html", template_params)
		self.response.write('Single word {}'.format(word))

app = webapp2.WSGIApplication([
	('/scoreboard[\/]?', BoardHandler),
	('/scoreboard/(.*)', WordBoardHandler),
], debug=True)
