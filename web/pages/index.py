#from google.appengine.api import users
from google.appengine.ext.webapp import template

from models.user import User
import webapp2

class IndexHandler(webapp2.RequestHandler):
	def get(self):
		template_params = {}
		user = User.checkUser()
		if not user:
			template_params['loginUrl'] = User.loginUrl()
		else:
			template_params['logoutUrl'] = User.logoutUrl()
			template_params['user'] = user.email()
		
		html = template.render("web/templates/index.html", template_params)
		self.response.write(html)
#		user = users.get_current_user()
#
#		if user:
#			self.response.headers['Content-Type'] = 'text/plain'
#			self.response.write('Hello, ' + user.nickname())
#		else:
#			self.redirect(users.create_login_url(self.request.uri))

		#self.response.write('Hello world!')

app = webapp2.WSGIApplication([
	('/', IndexHandler)
], debug=True)
