"""This module includes functions for profile page,
like getting post count, thread count and user data."""
from flask import redirect, render_template, session
from app import app
from src.profile.profile_context import (
    get_user_info,
    get_thread_count,
    get_like_count,
    get_poll_count,
    get_post_count,
)

@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect("/login")  # Redirect to login if not logged in

    username = session['username']
    user = get_user_info(username)

    if user:
        # Fetch thread count for the user
        thread_count = get_thread_count(user.username)

        # Fetch post count for the user
        post_count = get_post_count(user.username)

        #Fetch like count for the user
        like_count = get_like_count(user.username)

        poll_count = get_poll_count(user.username)

        return render_template("profile.html",
            thread_count=thread_count,
            post_count=post_count,
            user=user,
            like_count=like_count,
            poll_count=poll_count
            )
    return render_template("profile.html",
        thread_count=0,
        post_count=0,
        user=None,
        like_count=0,
        poll_count= 0
        )
