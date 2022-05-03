from flask import render_template, redirect, url_for, flash, abort, current_app
from flask_login import login_required
import random
from shorten import db
from shorten.models import ShortenedURL
from . import main
from .forms import EditURLForm, URLForm, DeleteURLForm, MultiSelectURLForm
from datetime import datetime

@main.route('/', methods=['GET','POST'])
@login_required
def index():
    form = URLForm()
    urls = ShortenedURL.query.order_by(ShortenedURL.modification_date.desc()).all()
    delform = DeleteURLForm(prefix='delete--')
    msform = MultiSelectURLForm(prefix='multi--')
    msform.boxes.choices = [(u.slug,u.slug) for u in urls]
    editform = EditURLForm()

    if editform.submit.data:
        if editform.validate_on_submit():
            su = ShortenedURL.query.filter_by(slug=editform.oldslug.data).first()
            su.slug = editform.newslug.data
            su.dest = editform.dest.data
            su.modification_date = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('main.index'))


    elif msform.submit.data and msform.validate_on_submit():
        error=False
        for slug in msform.boxes.data:
            su = ShortenedURL.query.filter_by(slug=slug).first()
            if su is None:
                flash("Not all selected URL values exist anymore. Please try again.")
                error=True
            else:
                db.session.delete(su)
            db.session.commit()
        if error:
            flash("Not all selected URLs could be deleted.", "select_error")

        return redirect(url_for('main.index'))

    elif delform.slug.data:
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
            su.modification_date = datetime.utcnow()
            db.session.add(su)
            db.session.commit()
            return redirect(url_for('main.index'))
    base = current_app.config['SERVER_NAME'] + current_app.config['BASE_URL']
    if base[-1] != '/':
        base += '/'
    return render_template('index.html', form=form, delform=delform,
                           msform=msform, editform=editform, urls=urls, base=base, zip=zip)

@main.route('/<slug>')
def forward(slug):
    su = ShortenedURL.query.filter_by(slug=slug).first()
    if su is None:
        abort(404)
    return redirect(su.dest)

