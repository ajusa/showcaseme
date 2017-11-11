from showcaseme import users, listings, TAGS
from flask_login import UserMixin
from tinydb import Query
from collections import Counter, OrderedDict
def getUserData(id):
	User = Query()
	if users.search(User.id == id):
		return users.search(User.id == id)[0]
	else: 
		return None
def getListingData(id):
	q = Query()
	if listings.search(q.id == str(id)):
		return listings.search(q.id == str(id))[0]
	else: 
		return None
class User(UserMixin):
	def __init__(self, uid, user_type=''):
		self.id = uid
		if 'userType' in getUserData(uid):
			self.userType = getUserData(uid)['userType']
		else:
			self.userType = user_type
		self.name = getUserData(uid)['name']

#returns a dictionary {userID: matchPercent} where match is a decimal between 0.0 and 1.0, where 1.0 is a perfect match and 0.0 is a total miss. Only returns users that are above a certain threshold
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

def listingSearchOld(requirements, bonusReqs=[], requirementWeight=1.0, bonusWeight=0.5, threshold=0.3, limit=0):
	foundListings = {}
	requirements = {key: int(requirements[key]) for key in requirements}
	bonusReqs = {key: int(bonusReqs[key]) for key in bonusReqs}
	maxPoints = requirementWeight * sum([1+val for val in requirements.values()]) + bonusWeight * sum([1+val for val in bonusReqs.values()])
	for listing in listings.all():
		if not maxPoints:
			foundListings = {listing['id']: 1.0 for listing in listings.all()}
			break
		points = 0.0
		listingTags = {tag['name']: tag['skill'] for tag in listing['tags']}
		for tag in listingTags.keys():  #assign points to each listing
			if tag in requirements:
				if listingTags[tag] > requirements[tag]:
					points += requirementWeight * (1+requirements[tag])
				else: #listing skill <= required skill
					points += requirementWeight * (1+listingTags[tag])
			elif tag in bonusReqs:
				if listingTags[tag] > bonusReqs[tag]:
					points += bonusWeight * (1+bonusReqs[tag])
				else: #listing skill <= required skill
					points += bonusWeight * (1+listingTags[tag])#"""
		if points/maxPoints >= threshold:
			foundListings[listing['id']] = points/maxPoints
	if limit:
		foundListings = dict(Counter(foundListings).most_common(limit))
	#print(foundListings)
	return foundListings

def listingSearch(requirements, bonusReqs=[], requirementWeight=1.0, bonusWeight=0.5, threshold=0.3, limit=0):
	foundListings = {}
	requirements = {key: int(requirements[key]) for key in requirements}
	bonusReqs = {key: int(bonusReqs[key]) for key in bonusReqs}
	for listing in listings.all():
		listingTags = {tag['name']: tag['skill'] for tag in listing['tags']}
		bonusTags = {tag['name']: tag['skill'] for tag in listing['bonus_tags']}
		maxPoints = maxListingScore(listingTags, bonusTags, requirementWeight=requirementWeight, bonusWeight=bonusWeight)
		print(listing['title'])
		print(maxPoints)
		points = 0
		for tag in listingTags.keys():
			if tag in requirements:
				if listingTags[tag] > requirements[tag]:
					points += (listingTags[tag] - requirements[tag]) * requirementWeight
				else: #listing skill <= searched (possessed) skill
					pass #no penalty
			else:
				points += 3 * requirementWeight #maximum number of penalty points
		for tag in bonusTags.keys():
			if tag in requirements:
				if bonusTags[tag] > requirements[tag]:
					points += (bonusTags[tag] - requirements[tag]) * bonusWeight
				else: #listing skill <= searched (possessed) skill
					pass #no penalty
			else:
				points += 3 * bonusWeight #maximum number of penalty points
		print(points)
		if not maxPoints:
			continue
		if ((maxPoints - points)/maxPoints) >= threshold:
			foundListings[listing['id']] = ((maxPoints - points)/maxPoints)
		print("\n" + listing['title'])
		print("{0} - {1}/{0}".format(maxPoints, points))
		print(((maxPoints - points)/maxPoints))#"""
	if limit:
		foundListings = dict(Counter(foundListings).most_common(limit))
	print(foundListings)
	return foundListings

def maxListingScore(requirements, bonuses, requirementWeight=1.0, bonusWeight=0.5):
	maxPoints = 0
	for tag in requirements.keys():
		maxPoints += (requirements[tag]+1) * requirementWeight
	for tag in bonuses.keys():
		maxPoints += (bonuses[tag]+1) * bonusWeight
	return maxPoints


def topSkills(limit):
	skills = {}
	for listing in listings.all():
		listingTags = {tag['name']: tag['skill'] for tag in listing['tags']}
		for tag in (str(tag) for tag in listingTags.keys()):
			if tag not in skills.keys(): #add new tag to list
				skills[tag] = {0:0, 1:0, 2:0, 'total':0}
			#Increase the count of the right skill level of the right tag by 1
			skills[tag][listingTags[tag]] += 1
			#increase total level (for sorting)
			skills[tag]['total'] += 1
	#sort the skills
	skillTotals = {tag:skills[tag]['total'] for tag in skills.keys()}
	sortedSkills = OrderedDict(Counter(skillTotals).most_common(limit))
	#print(sortedSkills)
	"""
		{'Python': {0: 0, 1: 0, 2: 2, 'total': 2}, 'C++': {0: 0, 1: 2, 2: 0, 'total': 2}, 'Web Development': {0: 2, 1: 0, 2: 0, 'total': 2}}
	"""
	sortedSkillLevels = {skill:skills[skill] for skill in sortedSkills}
	formatted = [{'name': "Underlying Understanding", 'color':"rgba(240, 241, 244, 0.9)", 'data':[ [ skill, sortedSkillLevels[skill][0] ] for skill in sortedSkills.keys() ]}, 
		{'name': "Passable Proficiency", 'color':"rgba(255, 215, 0, 0.9)", 'data':[ [ skill, sortedSkillLevels[skill][1] ] for skill in sortedSkills.keys() ]},
		{'name': "Extensive Experience", 'color':"rgba(0, 120, 215, 0.9)", 'data':[ [ skill, sortedSkillLevels[skill][2] ] for skill in sortedSkills.keys() ]}
	]
	#print("Formatted:", formatted)
	return formatted