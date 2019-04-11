from functools import wraps
from flask import Flask, render_template, flash, session, url_for, g, redirect, request


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user') is None:
            return redirect(url_for('.index'))

        return view(**kwargs)

    return wrapped_view

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_NAME='portal',
        DB_USER='portal_user',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import db
    db.init_app(app)

    @app.route('/', methods=('GET', 'POST'))
    def index():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            #have an error
            error = None
            conn = db.get_db()
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE email = %s;', (email,)
            )
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user is None:
                # throw an error
                error = 'Incorrect email'
                flash(error)
            elif user[2] != password:
                error = 'Incorrect password'
                flash(error)
            else:
                session.clear()
                session['user'] = user


                return redirect(url_for('home'))

        # if a post has happened i want to go to a new template(view)
        return render_template('index.html')

    @app.route('/home')
    @login_required
    def home():
        return render_template('home.html')


    @app.route('/logout')
    # @login_required
    def logout():
        session.clear()
        return redirect(url_for('index'))

    return app
