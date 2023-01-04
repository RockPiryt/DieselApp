# diesel_api/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy # do łatwej obsługi baz danych
from flask_migrate import Migrate # do migracji baz danych
from flask_login import LoginManager # do logowania usera

app = Flask(__name__)

app.config['SECRET_KEY']='mysecret'

#############DATABASE SETUP#######
basedir = os.path.abspath(os.path.dirname(__file__))#set up base directory
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir, 'data.sqlite')#set up connection to database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

##################
#LOGIN CONFIG
login_manager=LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login' # określenie view do logowania, potem będzie blueprint na to

#################

from diesel_api.core.views import core
from diesel_api.trip_calculator.views import trip
from diesel_api.diesel_cars.views import car
from diesel_api.error_pages.handlers import error_pages
from diesel_api.users.views import users

app.register_blueprint(core)
app.register_blueprint(trip)
app.register_blueprint(car)
app.register_blueprint(error_pages)
app.register_blueprint(users)