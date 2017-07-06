from flask import Flask, Response, redirect, url_for, request, session, abort, render_template, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 
from flask_cors import CORS, cross_origin
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
app = CustomFlask(__name__)
app.config.update(DEBUG = True,SECRET_KEY = 'secret_xxx')
CORS(app)
# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
users  = {}
product = [{"source": "walmart", "price": 50, "title": "Trolls Vehicle"}, {"source": "walmart", "price": 60, "title": "Trolls Vehicle"}]
class User(UserMixin):
    def __init__(self, uid):
        self.id = uid
        self.name = users[self.id]['name']
@app.route('/')
#@login_required
def home():
    return render_template('home.html', data=product)
@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template('signup.html')
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        uid = request.get_json()['uid']
        if uid in users:
            user = User(uid)
            login_user(user)
            return jsonify(result='ok')
        else:
            users[uid] = {'name': request.get_json()['name']}
            user = User(uid)
            login_user(user)
            return jsonify(result='ok')
    else:
        return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')  
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
	if userid in users:
		return User(userid)   
if __name__ == "__main__":
    app.run()