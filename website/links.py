from flask import Blueprint, render_template, redirect, request, flash, jsonify, url_for
from flask_login import login_required, current_user

from website.utils import create_random_string, is_url
from . import db
from .models import Link

links = Blueprint('links', __name__)

@links.route('/')
@login_required
def index():
    links = Link.query.filter_by(user_id=current_user.id).order_by(Link.date_created.desc()).all()
    return render_template('links/links.html', user=current_user, links=links)

@links.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    errors = {}
    if request.method == 'POST':
        title = request.form.get('title').strip()
        url = request.form.get('url').strip()
        status = request.form.get('status')

        status = 'private' if status != 'on' else 'public'
        
        if not is_url(url):
            errors['url'] = 'URL is not valid, using (http, https) protocol.'
        if not title:
            errors['title'] = 'Title must be not empty.'
        if not url:
            errors['url'] = 'URL must be not empty.'

        shorten_url = create_random_string()

        while True:
            link = Link.query.filter_by(shorten_url=shorten_url).first()
            if not link:
                break

        if len(errors) == 0:
            new_link = Link(title=title, url=url, status=status, shorten_url=shorten_url, user_id=current_user.id)
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

@links.route('/<int:link_id>/status', methods=['PUT'])
@login_required
def set_status(link_id):
    link = Link.query.get(link_id)

    if not link:
        return jsonify({'message': 'Link does not exist.'}), 404
    elif current_user.id != link.user_id:
        return jsonify({'message': 'You don\'t have permission to update this link.'}), 403

    link.status = 'private' if link.status == 'public' else 'public'
    db.session.commit()
    return jsonify({'message': 'Link successfully updated.', 'current_status': link.status}), 200


@links.route('/<int:link_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(link_id):
    errors = {}
    link = Link.query.get(link_id)
    if request.method == 'POST':
        title = request.form.get('title').strip()
        url = request.form.get('url').strip()
        status = request.form.get('status')

        status = 'private' if status != 'on' else 'public'
        
        if not is_url(url):
            errors['url'] = 'URL is not valid, using (http, https) protocol.'
        if not title:
            errors['title'] = 'Title must be not empty.'
        if not url:
            errors['url'] = 'URL must be not empty.'

        if len(errors) == 0:
            link.title = title
            link.status = status
            link.url = url
            db.session.commit()
            flash('Link successfully edited.', category='success')
            return redirect(url_for('links.index'))


    if not link:
        flash('Link does not exist.', category='error')
    elif current_user.id != link.user_id:
        flash('You don\'t have permission to edit this link.', category='error')
    else:
        return render_template('links/edit.html', user=current_user, errors=errors, link=link)

    return redirect(url_for('links.index'))