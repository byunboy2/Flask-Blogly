"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Users"""
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False, unique=False)
    last_name = db.Column(db.String(50), nullable=False, unique=False)
    image_url = db.Column(db.String(500), nullable=False, unique=False)

    # direct navigation: user to .posts and back

class Post(db.Model):
    """Posts"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, unique=False)
    content = db.Column(db.String(10000), nullable=False, unique=False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # direct navigation: .posts to user and back

    user = db.relationship('User',backref = 'posts')
