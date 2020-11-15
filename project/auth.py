# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from sqlalchemy import update, create_engine
from . import db

import os

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    if "user_id" in session:
        return redirect(url_for('main.profile'))
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    session['user_id'] = user.id
    session['root_folder'] = user.root_folder
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()  # if this returns a user, then the email already exists in
    # database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    # ignore the error
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # creating folder for new user
    os.chdir(r"C:\Users\param\OneDrive\Desktop\bandta")
    folder_name = os.path.join(r"C:\Users\param\OneDrive\Desktop\bandta", "user_" + str(new_user.id))
    os.mkdir(folder_name)
    new_user.root_folder = folder_name
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop("user_id", None)
    session.pop("root_folder", None)
    return redirect(url_for('main.index'))
