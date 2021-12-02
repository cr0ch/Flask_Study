from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

basedir = os.path.abspath(os.path.dirname(__file__))


my_app = Flask(__name__)
my_app.config['SECRET_KEY'] = '12345'
my_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

db = SQLAlchemy(my_app)
migrate = Migrate(my_app, db)
login_manager = LoginManager(my_app)
login_manager.login_view = 'login'
from app import routes



