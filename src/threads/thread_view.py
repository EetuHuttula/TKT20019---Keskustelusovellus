"""This module includes functions for getting
theads to frontpage"""
from flask import render_template
from sqlalchemy import text
from app import app
from db import db
import os


@app.route("/", methods=["GET", "POST"])
def index():
    query = text("""
        SELECT
        t.id,
        t.title, 
        t.content, 
        t.creation_date,
        t.user_username,
        t.media_path,
        COUNT(DISTINCT l.id) AS like_count,
        COUNT(DISTINCT p.id) AS post_count
        FROM threads t
        LEFT JOIN likes l ON t.id = l.thread_id
        LEFT JOIN posts p ON t.id = p.thread_id
        GROUP BY t.id, t.title, t.content, t.creation_date, t.user_username, t.media_path
    """)
    
    result = db.session.execute(query)
    threads = result.fetchall()
    return render_template("frontpage.html", threads=threads)
