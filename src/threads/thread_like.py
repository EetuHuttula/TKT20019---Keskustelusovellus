"""This module includes function for liking the threads"""
from flask import redirect, session, url_for, flash
from sqlalchemy import text
from app import app
from db import db

@app.route("/like/<int:thread_id>", methods=["POST"])
def like(thread_id):
    username = session.get("username")

    if not username:
        flash("You must be logged in to like a thread.", "error")
        return redirect("/login")

    # Check if the user has already liked the thread
    query_existing_like = text(
    """SELECT id, user_username, thread_id FROM likes WHERE
    user_username = :username AND
    thread_id = :thread_id""")
    result_existing_like = db.session.execute(query_existing_like,
    {"username": username, "thread_id": thread_id})
    existing_like = result_existing_like.fetchone()

    if existing_like:
        flash("You have already liked this thread.", "error")
    else:
        # Add a new like
        query_new_like = text(
        """INSERT INTO likes 
        (user_username, thread_id) 
        VALUES (:username, :thread_id)""")

        db.session.execute(query_new_like,
        {"username": username, "thread_id": thread_id})

        db.session.commit()
        flash("You liked the thread!", "success")
    return redirect(url_for("index"))
