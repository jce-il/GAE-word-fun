#from google.appengine.api import users
from google.appengine.ext.webapp import template

from models.user import User
import webapp2

class FourOFourHandler(webapp2.RequestHandler):
	#we provide args=None becuase that's how webapp2 treats the (.*) in /(.*)
	def get(self, args=None):
		template_params = {"args":args}
		user = User.checkUser()
		if not user:
			template_params['loginUrl'] = User.loginUrl()
		else:
			template_params['logoutUrl'] = User.logoutUrl()
			template_params['user'] = user.email
			
		html = template.render("web/templates/404.html", template_params)
		self.response.write(html)

app = webapp2.WSGIApplication([
	('/(.*)', FourOFourHandler)
], debug=True)
