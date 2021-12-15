from re import template
from flask.templating import render_template
from flask_login import login_required
from app import my_app, db
import datetime
from flask_login import current_user, login_user, logout_user
from flask import render_template, redirect, url_for, request
from app.models import User


@my_app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    
    if request.method=='POST':
        form = request.form
        inputed_username = form.get('username')
        inputed_password = form.get('password')
        inputed_email = (form.get('email'))
        
        user = User(username=inputed_username, email=inputed_email)
        user.set_password(inputed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    else:
        return render_template("register.html")
        
        
        


@my_app.route('/date')
@login_required
def get_date():
    date = str(datetime.datetime.now())
    return render_template("date.html", time = date)
    

@my_app.route('/')
@my_app.route('/index')
@login_required
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

@my_app.route('/user/<username>')
@login_required
def user(username):
    user_from_db = User.query.filter_by(username=username).first_or_404()
    
    return render_template('user_profile.html', user=user_from_db)

@my_app.errorhandler(404)
def error_handler_404(error):
    return render_template('404.html'), 404 

@my_app.errorhandler(500)
def error_handler_500(error):
    db.session.rollback()
    return render_template('500.html'), 500

@my_app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.datetime.utcnow()
        db.session.commit()

@my_app.route('/edit_profile', methods=['POST','GET']) 
@login_required
def edit_profile():
    if request.method == 'GET':
        return render_template("edit_profile.html")
    elif request.method == 'POST':
        form = request.form
        inputed_new_username = form.get('new_username')
        inputed_about_me = form.get('about_me').strip( )
        if inputed_new_username.isalnum(): 
            current_user.username = inputed_new_username
        # TODO Сделать сообщение об ошибке
        current_user.about_me = inputed_about_me
        db.session.commit()
        print(inputed_about_me)
        print(inputed_new_username)
        return redirect(url_for('user', username = current_user.username))

        





     
    