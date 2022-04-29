from flask import url_for, render_template, redirect, flash, request
from flask_login import login_user, logout_user
from werkzeug.urls import url_parse
from . import auth
from .. import db
from .forms import LoginForm, SetupForm
from ..models import User

@auth.route('/login', methods=['GET','POST'])
def login():
    if User.query.count() == 0:
        flash('Please set up an admin account first.')
        return redirect(url_for('auth.setup'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Username or password incorrect.')
            return redirect(url_for('auth.login'))
        else:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc!='':
                next_page = url_for('main.index')
            return redirect(next_page)
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/setup', methods=['GET', 'POST'])
def setup():
    if User.query.count() > 0:
        return redirect(url_for('auth.login'))
    form = SetupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome, {user.username}. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('auth/setup.html', form=form)

