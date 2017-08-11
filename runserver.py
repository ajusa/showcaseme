import os
from subprocess import call
if __name__ == '__main__':
	os.environ["FLASK_APP"] = "showcaseme/__init__.py"
	os.environ["FLASK_DEBUG"] = "1"
	call("flask run", shell=True)

