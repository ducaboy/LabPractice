import sqlite3
from datetime import datetime

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:                               #g is a special objects which handles the sb requests
        g.db = sqlite3.connect(                     #if db is not included in g we configure a sql database
            current_app.config['DATABASE'],         #otherwise we just return the databse
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db() #return a db connection with a relative path to the sql schema

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def init_app(app):
    app.teardown_appcontext(close_db)  #all the previous functions need to be registered in the app
    app.cli.add_command(init_db_command)#sp we call them once the app is created and given as parameter


@click.command('init-db')
def init_db_command(): #CALLS THE PREVIOUS FUNCTIONS 
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)