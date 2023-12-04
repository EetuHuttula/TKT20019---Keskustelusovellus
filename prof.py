"""This module includes functions for profile page,
like getting post count, thread count and user data."""
from flask import redirect, render_template, session
from sqlalchemy import text
from app import app
from db import db

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

        #Fetch like count for the user
        like_count = get_like_count(user.username)

        return render_template('profile.html',
            thread_count=thread_count,
            post_count=post_count, user=user, like_count=like_count)
    return render_template('profile.html',
        thread_count=0, post_count=0, user=None, like_count=0)

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

def get_like_count(username):
    query = text("SELECT COUNT(*) FROM likes WHERE user_username=:username")
    result = db.session.execute(query, {"username": username})
    like_count = result.scalar()
    return like_count
