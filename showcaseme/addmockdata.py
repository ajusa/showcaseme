import json
from tinydb import TinyDB
from flask import jsonify
db = TinyDB('main.db')
listings = db.table('listings')
users = db.table('users')
def addMockdata():
	raw = open("mockdata.json").read()
	data = json.loads(raw)
	for user in data:
		users.insert(user)
	return True
if __name__ == '__main__':
	if addMockdata():
		print 'OK'