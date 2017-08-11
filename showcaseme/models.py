from showcaseme import users
from flask_login import UserMixin
from tinydb import Query
from collections import Counter
def getUserData(id):
	User = Query()
	if users.search(User.id == id):
		return users.search(User.id == id)[0]
	else: 
		return False

class User(UserMixin):
	def __init__(self, uid, user_type=''):
		self.id = uid
		if 'userType' in getUserData(uid):
			self.userType = getUserData(uid)['userType']
		else:
			self.userType = user_type
		self.name = getUserData(uid)['name']

#returns a dictionary {userID: matchPercent} where match is a decimal betweeon 0.0 and 1.0, where 1.0 is a perfect match and 0.0 is a total miss. Only returns users that are above a certain threshold
def userSearch(requirements, bonusReqs=[], requirementWeight=1.0, bonusWeight=0.5, threshold=0.3, limit=0):
	foundUsers = {}
	requirements = {key: int(requirements[key]) for key in requirements}
	bonusReqs = {key: int(bonusReqs[key]) for key in bonusReqs}
	maxPoints = requirementWeight * sum([1+val for val in requirements.values()]) + bonusWeight * sum([1+val for val in bonusReqs.values()])
	for user in users.all():
		if not maxPoints:
			foundUsers = {user['id']: 1.0 for user in users.all()}
			break
		points = 0.0
		if not 'profile' in user:
			continue
		userTags = {tag['name']: tag['skill'] for tag in user['profile']['tags']}
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
		if points/maxPoints >= threshold:
			foundUsers[user['id']] = points/maxPoints
	if limit:
		foundUsers = dict(Counter(foundUsers).most_common(limit))
	return foundUsers
