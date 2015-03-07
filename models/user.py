#this model represents a user in our system

from google.appengine.api import users
from google.appengine.ext import ndb

class User(ndb.Model):
	email = ndb.StringProperty()
	
	
	@staticmethod
	def checkUser():
		googleUser = users.get_current_user()
		if not googleUser:
			return False
		
		user = User.query(User.email == googleUser.email()).get()
		if user:
			return user
		
		return False
	
	#generates a url at which the user can login, and then will be redirected back to his original location
	@staticmethod
	def loginUrl():
		return users.create_login_url('/connect')
	
	#generates a url at which the user can logout, and then will be redirected back to his original location
	@staticmethod
	def logoutUrl():
		return users.create_logout_url('/')
	
	@staticmethod
	def connect():
		googleUser = users.get_current_user()
		if googleUser:
			user = User.query(User.email == googleUser.email()).get()
			if not user:
				user = User()
				user.email = googleUser.email()
				user.put()
			return user

		else:
			return "not connected"