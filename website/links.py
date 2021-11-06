from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from . import db
from .models import Link

links = Blueprint('links', __name__)

@links.route('/')
@login_required
def index():
    links = Link.query.order_by(Link.date_created.desc()).all()
    return render_template('links/links.html', user=current_user, links=links)

@links.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    errors = {}
    if request.method == 'POST':
        title = request.form.get('title').strip()
        url = request.form.get('url').strip()

        if not title:
            errors['title'] = 'Title must be not empty.'
        if not url:
            errors['url'] = 'URL must be not empty.'

        if len(errors) == 0:
            new_link = Link(title=title, url=url, shorten_url=url, user_id=current_user.id)
            db.session.add(new_link)
            db.session.commit()
            flash('Link successfully created.', category='success')
            return redirect(url_for('links.index'))

    return render_template('links/create.html', user=current_user, errors=errors)