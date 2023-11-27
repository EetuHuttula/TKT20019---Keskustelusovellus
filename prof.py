from app import app
from flask import redirect, render_template, request, session, url_for, flash
from db import db
from sqlalchemy import text 

@app.route("/profile")
def profile():
    if 'username' not in session:
        return redirect('/login')  # Redirect to login if not logged in

    username = session['username']
    user = get_user_info(username)

    if user:
        # Fetch thread count for the user
        thread_count = get_thread_count(user.username)

        # Fetch post count for the user
        post_count = get_post_count(user.username)

        return render_template('profile.html', thread_count=thread_count, post_count=post_count, user=user)
    else:
        # Handle the case when the user is not found
        return render_template('profile.html', thread_count=0, post_count=0, user=None)

# Function to retrieve user information from the database
def get_user_info(username):
    query = text("SELECT * FROM users WHERE username=:username")
    result = db.session.execute(query, {"username": username})
    user = result.fetchone()
    return user

# Function to get thread count for a user
def get_thread_count(username):
    query = text("SELECT COUNT(*) FROM threads WHERE user_username=:username")
    result = db.session.execute(query, {"username": username})
    thread_count = result.scalar()  # scalar() fetches the count value
    return thread_count

# Function to get post count for a user
def get_post_count(username):
    query = text("SELECT COUNT(*) FROM posts WHERE user_username=:username")
    result = db.session.execute(query, {"username": username})
    post_count = result.scalar()  # scalar() fetches the count value
    return post_count