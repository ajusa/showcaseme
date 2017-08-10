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
	def __init__(self, uid, user_type='student'):
		self.id = uid
		self.userType = user_type
		self.name = getUserData(uid)['name']

#returns a dictionary {userID:match} where match is a decimal betweeon 0.0 and 1.0, where 1.0 is a perfect match and 0.0 is a total miss. Only returns users that are above a certain threshold
def userSearch(requirements, bonusReqs=[], requirementWeight=1.0, bonusWeight=0.5, threshold=0.3):
	foundUsers = {} 
	for user in users.all():
		points = 0.0
		userTags = {tag['name']: tag['skill'] for tag in user['profile']['tags']}
		requirements = {tag['name']: tag['skill'] for tag in requirements}
		bonusReqs = {tag['name']: tag['skill'] for tag in bonusReqs}
		maxPoints = requirementWeight * sum([1+val for val in requirements.values()]) + bonusWeight * sum([1+val for val in bonusReqs.values()])
		for tag in userTags.keys():
			if tag in requirements:
				if userTags[tag] > requirements[tag]:
					points += requirementWeight * (1+requirements[tag])
				else: #User skill <= required skill
					points += requirementWeight * (1+userTags[tag])
			elif tag in bonusReqs:
				if userTags[tag] > bonusReqs[tag]:
					points += bonusWeight * (1+bonusReqs[tag])
				else: #User skill <= required skill
					points += bonusWeight * (1+userTags[tag])
		if points/maxPoints > threshold:
			foundUsers[user.id] = points/maxPoints
	return foundUsers
