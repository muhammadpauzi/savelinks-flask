from flask import Blueprint, render_template, request
from flask.helpers import flash, url_for
from flask_login.utils import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from werkzeug.utils import redirect
from .models import User
from .utils import is_email, is_username
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('You are logged in.', category='success')
                return redirect(url_for('views.index'))

        flash('Login failed.', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    errors = {}
    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        repeat_password = request.form.get('repeat_password').strip()
        
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            errors['email'] = 'Email is already in use.'
        if username_exists:
            errors['username'] = 'Username is already in use.'
        if len(email) < 10:
            errors['email'] = 'Email is too short.'
        if len(username) < 10:
            errors['username'] = 'Username is too short.'
        if not is_username(username):
            errors['username'] = 'Username is must be only contain alpanumeric.'
        if not is_email(email):
            errors['email'] = 'Email is not valid.'
        if password != repeat_password:
            errors['repeat_password'] = 'Repeat password must be same with password.'
        if not email:
            errors['email'] = 'Email must be not empty.'
        if not username:
            errors['username'] = 'Username must be not empty.'
        if not password:
            errors['password'] = 'Password must be not empty.'

        if len(errors) == 0:
            new_user = User(email=email, username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash('Congratulation!!, Registration is successfully. Please login now!', category='success')
            return redirect(url_for('auth.login'))

    return render_template('register.html', errors=errors, user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))