from flask import render_template, redirect, url_for, flash, abort, current_app
from flask_login import login_required
import random
from shorten import db
from shorten.models import ShortenedURL
from . import main
from .forms import URLForm, DeleteURLForm
from datetime import datetime

@main.route('/', methods=['GET','POST'])
@login_required
def index():
    form = URLForm()
    delform = DeleteURLForm(prefix='delete--')
    
    if delform.slug.data:
        if delform.validate_on_submit():
            su = ShortenedURL.query.filter_by(slug=delform.slug.data).first()
            db.session.delete(su)
            db.session.commit()
        return redirect(url_for('main.index'))

    elif form.submit.data and form.validate_on_submit():
        su = ShortenedURL()
        su.dest = form.dest.data
        if form.custom.data == 'random':
            # try generating a random slug
            chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
            for _ in range(10):
                slug = ''.join(random.choice(chars) for __ in range(6))
                if ShortenedURL.query.filter_by(slug=slug).count() == 0:
                    break
            else:
                flash('A random slug could not be generated. Please try again'
                      ' or use a custom slug', 'add_url_error')
                slug = ''
        else:
            slug = form.customurl.data
        if slug:
            su.slug = slug
            su.creation_date = datetime.utcnow()
            db.session.add(su)
            db.session.commit()
            return redirect(url_for('main.index'))
    urls = ShortenedURL.query.order_by(ShortenedURL.creation_date.desc()).all()
    base = current_app.config['SERVER_NAME'] + current_app.config['BASE_URL']
    if base[-1] != '/':
        base += '/'
    return render_template('index.html', form=form, delform=delform, urls=urls, base=base)

@main.route('/<slug>')
def forward(slug):
    su = ShortenedURL.query.filter_by(slug=slug).first()
    if su is None:
        abort(404)
    return redirect(su.dest)

