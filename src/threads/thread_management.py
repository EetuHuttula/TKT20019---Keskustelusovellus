"""This module includes functions for editing threads and deleting them"""
from flask import redirect, render_template, request, session, url_for, flash
from sqlalchemy import text
from app import app
from db import db

@app.route("/edit_thread/<int:thread_id>", methods=["GET", "POST"])
def edit_thread(thread_id):
    # Check if user already has logged in
    if "username" not in session:
        return redirect("/login")

    if request.method == "POST":
        csrf_token = request.form.get("csrf_token")
        if csrf_token != session.get("csrf_token"):
            flash("Invalid CSRF token. Please try again.")
            return redirect(url_for("index"))
        
    #get thread from database
    query_thread = text(
    """SELECT id, title, content, creation_date,
    user_username FROM threads
    WHERE id = :thread_id""")
    result_thread = db.session.execute(query_thread, {"thread_id": thread_id})
    thread = result_thread.fetchone()

    #check if the user has made the thread
    if session['username'] != thread.user_username:
        flash("Cant edit another users thread")
        return redirect(url_for("index"))

    if request.method == "POST":
        #form handeling
        new_title = request.form['new_title']
        new_content = request.form['new_content']

        #update to database
        query_update_thread = text("""UPDATE threads SET title =
        :new_title, content = :new_content WHERE id = :thread_id""")
        db.session.execute(query_update_thread, {"new_title": new_title,
        "new_content": new_content, "thread_id": thread_id})
        db.session.commit()
        #after update, go back to index page
        return redirect(url_for('index', thread_id=thread_id))
    #render the edit.html
    return render_template('edit_thread.html', thread=thread)

@app.route("/delete_thread/<int:thread_id>", methods=["GET","POST"])
def delete_thread(thread_id):
    #check if user has logged in
    username = session.get("username")
    if not username:
        flash("You must be logged in to delete a thread.", "error")
        return redirect("/login")

    #get thread
    query_thread = text(
    """SELECT id, title, content,
    creation_date, user_username
    FROM threads WHERE id = :thread_id""")
    result_thread = db.session.execute(query_thread, {"thread_id": thread_id})
    selected_thread = result_thread.fetchone()

    if not selected_thread:
        flash("Thread not found.", "error")
        return redirect("/")

    #check if user has made the thread
    if username != selected_thread.user_username:
        flash("You are not the author of this thread.", "error")
        return redirect("/")

    #delete thread
    query_delete_thread = text("DELETE FROM threads WHERE id = :thread_id")
    db.session.execute(query_delete_thread, {"thread_id": thread_id})
    db.session.commit()

    flash("Thread deleted successfully.", "success")
    return redirect("/")
