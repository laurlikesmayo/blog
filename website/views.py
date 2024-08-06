from flask import Flask, Blueprint, render_template, request, url_for, redirect, session, flash, jsonify
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash 
from .models import Users
from flask_login import login_user, logout_user, login_required, UserMixin, current_user

import json

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
  
@views.route("/")
def home():
    return render_template('home.html')

@views.route("/about")
def about():
    return render_template('about.html')

@views.route("/coding")
def coding():
    return render_template('coding.html')

@views.route("/blog")
def blog():
    return render_template('blog.html')

@views.route("logout")
def logout():
    return render_template('logout.html')