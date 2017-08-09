from flask import Flask, g, Response, redirect, url_for, request, session, abort, render_template, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user , current_user
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
DEFAULT_COMPANY = {
	"name": "ACME widget corp",
	"company_desc": "Makes widgets",
	"listings": []
}
DEFAULT_LISTING = {
		"title": "Lead Widget Designer",
		"blurb": "Lead a team of 8 widget designers",
		"description": "Hover over me to edit this paragraph. ShowcaseMe supports Markdown in the editing popup as well!",
		"requirements": {"CAD": 2, "Leadership": 2, "C++": 1, "Public Speaking": 0},
		"bonus_reqs": {"Python": 2, "Java": 1},
		"compensation": "335k salary with sizeable bonuses. Perks include free food and state-of-the-art insurance."
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

#Server
import showcaseme.views
if __name__ == "__main__":
	app.run()