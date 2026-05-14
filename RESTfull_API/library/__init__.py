import os
from flask import Flask, request, Blueprint
from .books.controller import books
from .borrow.controller import borrow
from .extension import db, ma
from .model import Students, Books, Borrow, Category, Author


def create_db(app):
    with app.app_context():
        db.create_all()
        print("Database created successfully.")


def create_app(config_file=None):
    app = Flask(__name__)
    if config_file is None:
        config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.py")
    app.config.from_pyfile(config_file)
    db.init_app(app)
    ma.init_app(app)
    app.register_blueprint(books)
    app.register_blueprint(borrow)
    create_db(app)
    return app
