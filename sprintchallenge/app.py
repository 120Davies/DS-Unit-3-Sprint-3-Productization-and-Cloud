from flask import Flask

from .models import DB

#app factory
def create_app():
	app = Flask(__name__)

	#add config here:
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
	#add database init
	DB.init_app(app)
	#create route
	@app.route('/')

	#define function
	def root():
		return 'This is the home page.'

	return app
