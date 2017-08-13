import os
from showcaseme import app
import showcaseme.views
if __name__ == '__main__':
	os.environ["FLASK_APP"] = "showcaseme/__init__.py"
	os.environ["FLASK_DEBUG"] = "1"
	app.run()
