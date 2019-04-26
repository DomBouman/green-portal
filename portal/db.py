import os
import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash


def get_db():
    if 'db' not in g:
        # open a connection, save it to close when done
        DB_URL = os.environ.get('DATABASE_URL', None)
        if DB_URL:
            g.db = psycopg2.connect(DB_URL, sslmode='require')
        else:
            g.db = psycopg2.connect(
                f"dbname={current_app.config['DB_NAME']}" +
                f" user={current_app.config['DB_USER']}"
            )

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close() # close the connection


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        cur = db.cursor()
        cur.execute(f.read())
        cur.close()
        db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def create_user(email, password, role):


    conn = get_db()

    cur = conn.cursor()
    cur.execute("""
    INSERT INTO users (email, password, role)
    VALUES (%s, %s, %s);
    """, (email, generate_password_hash(password), role))
    conn.commit()
    cur.close()



# terminal command to create a user
# syntax: "flask create-user 'user@email' 'password' 'teacher' OR 'student'"
@click.command('create-user')
@click.argument('email')
@click.argument('password')
@click.argument('role')
@with_appcontext
def create_user_command(email, password, role):
    """create a new user"""
    if role != 'student' and role != 'teacher':
        click.echo("User role must be 'student' or 'teacher'")
    else:
        create_user(email, password, role)
        click.echo('Created user %s with the %s role' % (email, role))

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_user_command)
