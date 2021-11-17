from flask.templating import render_template
from app import my_app
import datetime
from flask import render_template



@my_app.route('/date')
def get_date():
    date = str(datetime.datetime.now())
    return render_template("date.html", time = date)

@my_app.route('/')
@my_app.route('/index')
def index():
    return render_template("index.html") 
    