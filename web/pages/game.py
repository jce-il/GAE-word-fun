#from google.appengine.api import users
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
		
		template_params['user'] = user.email
		
		word = Word.todaysWord()
		
		template_params['definition'] = word.definition
		
		html = template.render("web/templates/game.html", template_params)
		self.response.write(html)

app = webapp2.WSGIApplication([
	('/game', IndexHandler)
], debug=True)
