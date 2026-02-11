from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT r.id, title, rating, review, username, created, creator_id'
        ' FROM review r JOIN user u ON r.creator_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        rating = request.form['rating']
        author = request.form['author']
        review = request.form['review']
        error = None

        if not title:
            error = 'Title is required.'
        if not author:
            error = 'author is required.'    
        if not rating:
            error = 'Rating is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO review (title, rating, author, review ,creator_id)'
                ' VALUES (?, ?, ? , ?, ?)',
                (title, rating, author, review, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT r.id, title, review, rating, author, created, creator_id, username '
        'FROM review r JOIN user u ON r.creator_id = u.id '
        'WHERE r.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Review id {id} doesn't exist.")

    if check_author and post['creator_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        review = request.form['review']
        rating = request.form['rating']
        author = request.form['author']

        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE review SET title = ?, review = ?, rating = ?, author = ? '
                'WHERE id = ?',
                (title, review, rating, author, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM review WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))