import os
from subprocess import call
if __name__ == '__main__':
	os.environ["FLASK_APP"] = "showcaseme/__init__.py"
	call("flask run", shell=True)

