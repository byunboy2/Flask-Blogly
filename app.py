"""Blogly application."""

from flask import Flask, redirect, render_template, request
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
    return render_template("display_users.html", users=users)


@app.get("/users/new")
def add_user():
    """Add new user to list"""
    return render_template("add_user.html")


@app.post("/users/new")
def process_new_user():
    """Save new user information to database"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name = last_name , image_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int:user_id>")
def show_user_info(user_id):
    """Display information about user"""
    get_user = User.query.get_or_404(user_id)
    return render_template("user.html",user=get_user)

@app.get("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Shows edit page for user"""
    get_user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=get_user)

@app.post("/users/<int:user_id>/edit")
def save_edit(user_id):
    """Saves edit to database"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    get_user = User.query.get_or_404(user_id)
    get_user.first_name = first_name
    get_user.last_name = last_name
    get_user.image_url = image_url

    db.session.add(get_user)
    db.session.commit()

    return redirect ("/")

@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete user from database"""
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect("/")
