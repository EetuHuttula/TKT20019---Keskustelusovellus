"""This module includes functions for creating threads and posting to specific theards"""
from flask import redirect, render_template, request, session, url_for, flash
from sqlalchemy import text
from app import app
from db import db

@app.route("/thread/<int:thread_id>", methods=["GET", "POST"])
def view_thread(thread_id):
    if request.method == "GET":
        # Fetch the thread and its posts using direct SQL queries
        query_thread = text(
        """SELECT t.id, t.title, t.content,
            t.creation_date, t.user_username, t.media_path,
            COUNT(l.id) AS like_count
            FROM threads t
            LEFT JOIN likes l ON t.id = l.thread_id
            WHERE t.id = :thread_id
            GROUP BY t.id;
        """
        )
        result_thread = db.session.execute(query_thread, {"thread_id": thread_id})
        selected_thread = result_thread.fetchone()

        query_posts = text(
        """SELECT id, content, post_date,
        user_username, thread_id FROM posts
        WHERE thread_id = :thread_id""")
        result_posts = db.session.execute(query_posts, {"thread_id": thread_id})
        posts = result_posts.fetchall()

        return render_template("view_thread.html", thread=selected_thread, posts=posts)

    if request.method == "POST":
        # Handle the form submission for posting a reply
        content = request.form["content"]
        username = session.get("username")

        if not username:
            # Redirect to login or handle the case where the user is not logged in
            return redirect("/login")

        if not content or not content.strip():
            flash("Message can't be empty or contain only whitespace. Please try again.")
            return redirect(url_for("view_thread", thread_id=thread_id))

    if request.method == "POST":
        csrf_token = request.form.get("csrf_token")
        if csrf_token != session.get("csrf_token"):
            flash("Invalid CSRF token. Please try again.")
            return redirect(url_for("index"))

        # Insert the reply into the posts table using direct SQL query
        query_insert_post = text("""INSERT INTO posts (content, user_username, thread_id)
        VALUES (:content, :username, :thread_id)""")
        db.session.execute(query_insert_post, {"content": content,
        "username": username, "thread_id": thread_id})
        db.session.commit()
        return redirect(url_for("view_thread", thread_id=thread_id))
    return None





