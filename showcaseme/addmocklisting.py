import json
import uuid
from tinydb import TinyDB, Query
from flask import jsonify
from showcaseme.views import addListing, updateListing
db = TinyDB('../main.db')
listings = db.table('listings')
def addMockdata():
	raw = open("showcaseme/mocklistings.json").read()
	data = json.loads(raw)
	for listing in data:
		listingId = str(uuid.uuid4())
		listing['id'] = listingId
		url = addListing(listingId, "niQ5GHI1ZYdSAy4dF06UmWaKKq63")
		url.next()
		#listing['user'] = "niQ5GHI1ZYdSAy4dF06UmWaKKq63"
		q = Query()
		update = updateListing(listing, q)
		update.next()
	return True
if __name__ == '__main__':
	if addMockdata():
		print 'OK'