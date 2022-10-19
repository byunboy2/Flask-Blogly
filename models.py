"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
def connect_db(app):
    """Connect to database."""
    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __table__name = "User"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(50),nullable = False, unique = True)
    last_name = db.Column(db.String(50),nullable = False, unique = True)
    image_url = db.Column(db.String(50),nullable = False, unique = True)