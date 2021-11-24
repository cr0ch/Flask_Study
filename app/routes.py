from flask.templating import render_template
from app import my_app
import datetime
from flask_login import current_user, login_user, logout_user
from flask import render_template, redirect, url_for, request
from app.models import User



@my_app.route('/date')
def get_date():
    date = str(datetime.datetime.now())
    return render_template("date.html", time = date)

@my_app.route('/')
@my_app.route('/index')
def index():
    return render_template("index.html") 


@my_app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method=='POST':
        form = request.form
        inputed_username = form.get('username')
        inputed_password = form.get('password')
        remember = bool(form.get('remember'))
        user = User.query.filter_by(username=inputed_username).first()
        if user is None or not user.check_password(inputed_password): 
            # TODO flash message
            return redirect(url_for('login'))
        # else
        login_user(user, remember=remember)
        return redirect(url_for('index'))

    return render_template("login.html")


@my_app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
     
    