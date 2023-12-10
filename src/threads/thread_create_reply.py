"""This module includes functions for creating threads and posting to specific theards"""
from flask import redirect, render_template, request, session, url_for, flash
from sqlalchemy import text
from app import app
from db import db
from src.secrets_token import generate_csrf_token

@app.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    if request.method == 'GET':
        # Fetch the thread and its posts using direct SQL queries
        query_thread = text("SELECT * FROM threads WHERE id = :thread_id")
        result_thread = db.session.execute(query_thread, {"thread_id": thread_id})
        selected_thread = result_thread.fetchone()

        query_posts = text("SELECT * FROM posts WHERE thread_id = :thread_id")
        result_posts = db.session.execute(query_posts, {"thread_id": thread_id})
        posts = result_posts.fetchall()

        return render_template('view_thread.html', thread=selected_thread, posts=posts)

    if request.method == 'POST':
        # Handle the form submission for posting a reply
        content = request.form['content']
        username = session.get('username')

        if not username:
            # Redirect to login or handle the case where the user is not logged in
            return redirect('/login')

        if not content or not content.strip():
            flash("Message can't be empty or contain only whitespace. Please try again.")
            return redirect(url_for('view_thread', thread_id=thread_id))

        # Insert the reply into the posts table using direct SQL query
        query_insert_post = text("""INSERT INTO posts (content, user_username, thread_id)
        VALUES (:content, :username, :thread_id)""")
        db.session.execute(query_insert_post, {"content": content,
        "username": username, "thread_id": thread_id})
        db.session.commit()
        return redirect(url_for('view_thread', thread_id=thread_id))
    return None

@app.route("/send", methods=["POST"])
def send():

    if request.method == "POST":
        csrf_token = request.form.get("csrf_token")

    if not csrf_token:
        flash("CSRF token is missing. Please try again.")
        return redirect(url_for("index"))

    title = request.form["title"]
    content = request.form["content"]
    username = session.get("username")
      # Check if the user is logged in
    if not username:
        # Redirect to the login page or handle the case where the user is not logged in
        return redirect("/login")

    if not title or not title.strip() or not content or not content.strip():
        flash("Title or message can't be empty or contain only whitespace. Please try again.")
        return redirect(url_for("index"))

    # Insert the message into the database with the associated username
    sql = text("""INSERT INTO threads (title, content, user_username)
     VALUES (:title, :content, :user_username)""")
    db.session.execute(sql, {"title": title,
    "content": content, "user_username": username})
    db.session.commit()

    csrf_token = generate_csrf_token()
    return redirect('/', csrf_token=csrf_token)
