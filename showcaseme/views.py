from showcaseme import app, login_manager, users, db, DEFAULT_PROFILE, TAGS
from showcaseme.models import User, getUserData, userSearch
from tinydb import TinyDB, Query
from flask import Flask, g, Response, redirect, url_for, request, session, abort, render_template, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
@app.route('/')
def home():
	temp = []
	for item in users.all():
		if 'profile' in item:
			item['profile']['id'] = item['id']
			temp.append(item['profile'])
	return render_template('home.html', data=temp, tags = TAGS)
@app.route('/student/<id>')
def viewUser(id):
	user = getUserData(id)
	if 'profile' in user:
		return render_template('profile.html', data = user['profile'], tag = TAGS, id=id)
	return render_template('profile.html')
@app.route('/about')
def about():
	return render_template('about.html')
@app.route('/usertype')
def userType():
	return render_template('userType.html')
@app.route("/signup", methods=["GET"])
def signup():
	return render_template('signup.html')
@app.route("/login", methods=["GET", "POST"])
def login(): 
	if request.method == 'POST':
		uid = request.get_json()['uid']
		if getUserData(uid): #Means that they have an account
			user = User(uid)
			login_user(user)
			return jsonify(result='ok')
		else: #Means that this is their first time with us
			users.insert({'name': request.get_json()['name'], 'id': uid})
			user = User(uid)
			login_user(user)
			return jsonify(result='ok')
	else: #The login page for the form
		return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect("/")
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
	if request.method == 'POST':
		profile = request.get_json()
		person = Query()
		users.update({'profile': profile}, person.id == current_user.id)
		return jsonify(result='ok')
	else:
		user = getUserData(current_user.id)
		if 'profile' in user:
			return render_template('profile.html', data = user['profile'], tag = TAGS, id=current_user.id)
		else:
			DEFAULT_PROFILE['name'] = current_user.name
			return render_template('profile.html', data = DEFAULT_PROFILE, tag = TAGS, id=current_user.id)

@app.route("/search", methods=["GET"])
def search():
	found = userSearch(request.args)
	foundSorted = sorted(found, key=found.get, reverse=True)
	#print(request.args)
	#print([getUserData(user)['profile'] for user in sorted(found, key=found.get, reverse=True) if 'profile' in getUserData(user)])
	return render_template('search.html', data = [getUserData(user)['profile'] for user in foundSorted if 'profile' in getUserData(user)], 
		matches=[found[user] for user in foundSorted if 'profile' in getUserData(user)], tags = TAGS)

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
	return Response('<p>Login failed</p>')  
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
	if getUserData(userid):
		return User(userid)