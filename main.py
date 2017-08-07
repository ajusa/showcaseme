from flask import Flask, g, Response, redirect, url_for, request, session, abort, render_template, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user , current_user
from tinydb import TinyDB, Query
DEFAULT_PROFILE = {
	"name": "John Doe",
	"blurb": "Maker and Worker",
	"tags": [],
	"projects": [
	  {
		"title": "Work Experience",
		"blurb": "Lead Worker",
		"description": "Hover over me to edit this paragraph. ShowcaseMe supports Markdown in the editing popup as well!"
	  },
   ]
}
TAGS = lines = open("tags.txt").read().splitlines()
class CustomFlask(Flask):
	jinja_options = Flask.jinja_options.copy()
	jinja_options.update(dict(
		block_start_string='[%',
		block_end_string='%]',
		variable_start_string='[[',
		variable_end_string=']]',
		comment_start_string='[#',
		comment_end_string='#]',
		))
db = TinyDB('main.db')
listings = db.table('listings')
users = db.table('users')
app = CustomFlask(__name__)
app.config.update(DEBUG = True,SECRET_KEY = 'secret_xxx')
# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
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
@app.route('/')
def home():
	temp = []
	for item in users.all():
		if 'profile' in item:
			item['profile']['id'] = item['id']
			temp.append(item['profile'])
	return render_template('home.html', data=temp)
@app.route('/student/<id>')
def viewUser(id):
	user = getUserData(id)
	if 'profile' in user:
		return render_template('profile.html', data = user['profile'], tag = TAGS)
	return render_template('profile.html', )
@app.route('/about')
def about():
	return render_template('about.html')
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
		if 'profile' in user :
			return render_template('profile.html', data = user['profile'], tag = TAGS)
		else:
			DEFAULT_PROFILE['name'] = current_user.name
			return render_template('profile.html', data = DEFAULT_PROFILE)
# handle login failed
@app.errorhandler(401)
def page_not_found(e):
	return Response('<p>Login failed</p>')  
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
	if getUserData(userid):
		return User(userid)
if __name__ == "__main__":
	app.run()