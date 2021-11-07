from flask import Blueprint, render_template, redirect, request, flash, jsonify, url_for
from flask_login import login_required, current_user

from website.utils import is_url
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

        if not is_url(url):
            errors['url'] = 'URL is not valid, using (http, https) protocol.'
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

@links.route('/<int:link_id>/delete', methods=['DELETE'])
@login_required
def delete(link_id):
    link = Link.query.get(link_id)

    if not link:
        return jsonify({'message': 'Link does not exist.'}), 404
    elif current_user.id != link.user_id:
        return jsonify({'message': 'You don\'t have permission to delete this link.'}), 403

    db.session.delete(link)
    db.session.commit()
    return jsonify({'message': 'Link successfully deleted.'}), 200
