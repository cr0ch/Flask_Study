from re import template
from flask.templating import render_template
from flask_login import login_required
from app import my_app, db, mail
import datetime
from flask_login import current_user, login_user, logout_user
from flask import render_template, redirect, url_for, request, flash
from app.models import User, Post
import secrets
import string
import json
from flask_mail import Message




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
@my_app.route('/index/<int:page>')
@my_app.route('/index')
@login_required
def index(page=1):
    paginated_posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, 5, False)
    return render_template("index.html", posts=paginated_posts)
     


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
            flash('Invalid username or password')
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
@my_app.route('/user/<username>/<int:page>')
@login_required
def user(username, page=1):
    user_from_db = User.query.filter_by(username=username).first_or_404()
    user_posts = user_from_db.posts.order_by(Post.timestamp.desc()).paginate(page, 5, False)
    return render_template('user_profile.html', user=user_from_db, posts=user_posts)

@my_app.route("/delete_post/<int:post_id>")
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
    return redirect(request.referrer)
    

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

@my_app.route('/add_post', methods=['POST','GET']) 
@login_required
def add_post():
    if request.method == 'GET':
        return render_template("add_post.html")
    if request.method == 'POST':
        form = request.form
        text = form.get('text_post').strip()
        post = Post(text=text, timestamp=datetime.datetime.utcnow(), author=current_user)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('user', username = current_user.username))

@my_app.route('/reset_password', methods=['POST','GET'])
def reset_password():
    if request.method == 'GET':
        return render_template("reset_password.html")
    if request.method == 'POST':
        form = request.form
        email = form.get('email')
        user = User.query.filter_by(email=email).first()
        if user is None:
            return redirect(url_for('reset_password'))
        else:
            password = generator_password()
            send_mail(email, user.username, password)
            user.set_password(password)
            db.session.commit()
            return redirect(url_for('login'))

@my_app.route('/settings', methods=['POST','GET'])
def miscellaneous_information():
    if request.method == 'GET':
        return render_template("settings.html")
    if request.method == 'POST':
        form = request.form
    

def generator_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))
    return password

def send_mail(recipient, username, new_password):
    msg = Message('Reset password.[Microblog]', sender='Microblog', recipients=[recipient])
    msg.body = f'''
    Здравствуйте {username}!
    Вы запросили заявку на восстановление пароля.
    Вот и он: {new_password}'''
    mail.send(msg)

@my_app.route('/api/login', methods=['POST'])
def api_login():
    data = json.loads(request.data)
    
    user = User.query.filter_by(username=data['username']).first()
    if user is None or not user.check_password(data['password']): 
        return 'Invalid username or password', 400
    else:
        return 'Login ok', 200






    






        





     
    