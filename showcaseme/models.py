from showcaseme import users
from flask_login import UserMixin
from tinydb import Query
def getUserData(id):
	User = Query()
	if users.search(User.id == id):
		return users.search(User.id == id)[0]
	else: 
		return False
#listings.insert({"company": "Microsoft", "position": "Web Dev", "description": "Empower every person and every organization on the planet to achieve more."})
class User(UserMixin):
	def __init__(self, uid):
		self.id = uid
		self.name = getUserData(uid)['name']
def getCompanyData(id):
	company = Query()
	if companies.search(company.id == id):
		return companies.search(company.id == id)[0]
	else: 
		return False
class Company(UserMixin):
	def __init__(self, uid):
		self.id = uid
		self.name = getCompanyData(uid)['name']
