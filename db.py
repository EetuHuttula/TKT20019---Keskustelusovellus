"""This module is for db connection"""
from os import getenv
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy without an app to avoid circular imports
db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the Flask app"""
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
