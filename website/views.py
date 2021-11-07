from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required, current_user

from .models import Link

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def index():
    links = Link.query.all()
    return render_template('index.html', user=current_user, links=links)

@views.route('/<shorten_url>')
def redirect_to(shorten_url):
    link = Link.query.filter_by(shorten_url=shorten_url).first()

    # validation #1
    if not link:
        flash('Link does not exist.', category='error')
    # validation #2
    elif link.status != 'public' and link.user_id != current_user.id:
        flash('Link is private.', category='error')
    else:
        return redirect(link.url)

    # redirect for validation #1 & #2
    if current_user.is_authenticated:
        return redirect(url_for('links.index'))

    return redirect(url_for('auth.login'))
