"""Blogly application."""

from flask import Flask, redirect, render_template, request, flash
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blog_model'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'secrets, shhhh'

connect_db(app)
db.create_all()


@app.get("/")
def load_home():
    """Redirect to current list of users"""

    return redirect("/users")


@app.get("/users")
def load_user():
    """Load currently saved users"""

    users = User.query.all()  # order by users
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
    go_back = False

    if not first_name:
        flash("First name can't be empty")
        go_back = True
    if not last_name:
        flash("Last name can't be empty")
        go_back = True
    if not image_url:
        flash("Image url can't be empty")
        go_back = True

    if go_back:
        return render_template(
            "add_user.html",
            first_name=first_name,
            last_name=last_name,
            image_url=image_url
        )

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:user_id>")
def show_user_info(user_id):
    """Display information about user"""

    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)


@app.get("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Shows edit page for user"""

    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.post("/users/<int:user_id>/edit")
def save_edit(user_id):
    """Saves edit to database"""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete user from database"""

    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect("/")


@app.get("/users/<int:user_id>/posts/new")
def show_add_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("add_posts.html", user=user)


@app.post("/users/<int:user_id>/posts/new")
def add_post_for_user(user_id):

    title = request.form["title"]
    content = request.form["content"]

    user = User.query.get_or_404(user_id)
    
    post = Post(
        title=title,
        content=content,
        post_id=user.id
    )

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

