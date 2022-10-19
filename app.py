"""Blogly application."""

from flask import Flask, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blog_model'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get("/")

def load_home():
    """Redirect to current list of users"""
    return redirect("/users")

@app.get("/users")
def load_user():
    """Load currently saved users"""
    users = User.query.all()
    return render_template("index.html", users = users)