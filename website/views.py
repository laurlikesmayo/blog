from flask import Flask, Blueprint, current_app, render_template, request, url_for, redirect, session, flash, jsonify
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash 
from werkzeug.utils import secure_filename
from datetime import datetime
from .models import Users, Post
import os
from flask_login import login_user, logout_user, login_required, UserMixin, current_user
from . import app, db

views = Blueprint("views", __name__)
@views.route('/login',  methods=['GET', 'POST'] )
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        permanentsesh = request.form.get('permanentsession') == 'true' #returns bool
        user = Users.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=permanentsesh)
                print('Logged in')
                session.permanet = permanentsesh
                session['loggedin'] = True
                session['email'] = user.email
                flash('Log in sucessful', 'info ')
                return redirect(url_for('views.home')) 
            else:
                flash('Wrong Password')
        else:
            flash('Username does not exist')
                
                
    return render_template("login.html")

@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if not username or not password1:
            flash("Username or password cannot be empty!")
        elif len(password1) < 6 or len(username) < 6:
            flash("Username and password must contain at least 6 characters!")
        elif password1 != password2:
            flash("Passwords don't match!")
        else:
            username_exists = Users.query.filter_by(username=username).first()
            email_exists = Users.query.filter_by(email=email).first()
            if username_exists or email_exists:
                flash('Username or email already exists!')
            else:
                new_user = Users(username=username, email=email, password=generate_password_hash(password1))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                session['loggedin'] = True
                flash('Sign up successful', 'info')
                return redirect(url_for('views.personalize'))

    return render_template('register.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

@views.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        video_url = request.form.get('video_url')
        content = request.form.get('content')
        category = request.form.get('category')
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file and file.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

    
        new_post = Post(title=title, video_url=video_url, category=category, content=content, image_path=filename)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template('create_post.html')

@views.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)

@views.route("/")
def home():
    posts = Post.query.order_by(Post.date_added.desc()).limit(3).all()
    return render_template('home.html', posts=posts)

@views.route("/insights")
def insights():
    posts = Post.query.filter_by(category = 'insights')
    return render_template('insights.html', posts=posts)

@views.route("/coding")
def coding():
    posts = Post.query.filter_by(category='coding').all()
    return render_template('coding.html', posts=posts)

@views.route("/blog")
def blog():
    posts = Post.query.filter_by(category = 'blog')
    return render_template('blog.html', posts=posts)

@views.route("logout")
def logout():
    return render_template('logout.html')