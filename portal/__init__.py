from functools import wraps
from flask import Flask, render_template, flash, session, url_for, redirect, request, g
from werkzeug.security import check_password_hash

from .auth import login_required

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

    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/home')
    @login_required
    def home():
        return render_template('home.html')


    return app
