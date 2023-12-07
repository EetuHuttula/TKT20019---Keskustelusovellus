"""This module includes functions for getting
theads to frontpage"""
from flask import redirect, render_template, request, session, url_for
from sqlalchemy import text
from app import app
from db import db

@app.route("/", methods=["GET", "POST"])
def index():
    query = text("""
        SELECT t.*, COUNT(l.id) AS like_count
        FROM threads t
        LEFT JOIN likes l ON t.id = l.thread_id
        GROUP BY t.id
    """)
    result = db.session.execute(query)
    threads = result.fetchall()
    return render_template('frontpage.html', threads=threads)

def newthread():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        username = session.get("username")

        if not username:
            return redirect(url_for("login"))

        thread = thread(title=title, content=content, user_username=username)
        db.session.add(thread)
        db.session.commit()

    return redirect(url_for("index"))
