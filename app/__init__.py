from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from flask_mail import Mail

basedir = os.path.abspath(os.path.dirname(__file__))


my_app = Flask(__name__)
my_app.config['SECRET_KEY'] = '12345'
my_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
my_app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
my_app.config['MAIL_PORT'] = 587
my_app.config['MAIL_USE_TLS'] = True
my_app.config['MAIL_USERNAME'] = 'flaskmicroblog63@gmail.com'
my_app.config['MAIL_DEFAULT_SENDER'] ='flaskmicroblog63@gmail.com'
my_app.config['MAIL_PASSWORD'] = 'Flaskmicroblog123'

db = SQLAlchemy(my_app)
migrate = Migrate(my_app, db)
login_manager = LoginManager(my_app)
login_manager.login_view = 'login'
mail = Mail(my_app)
from app import routes





