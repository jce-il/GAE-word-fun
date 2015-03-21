#from google.appengine.api import users
from google.appengine.ext.webapp import template

from models.user import User
import webapp2

class IndexHandler(webapp2.RequestHandler):
	def get(self):
		template_params = {}
		user = User.connect()
		if not user:
			self.redirect('/')
		else:
			self.redirect('/game')

app = webapp2.WSGIApplication([
	('/connect', IndexHandler)
], debug=True)
