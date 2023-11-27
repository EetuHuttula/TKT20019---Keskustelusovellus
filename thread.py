from app import app
from flask import redirect, render_template, request, session, url_for, flash
from db import db
from sqlalchemy import text 

@app.route("/edit_thread/<int:thread_id>", methods=["GET", "POST"])
def edit_thread(thread_id):
    # Tarkista, onko käyttäjä kirjautunut sisään
    if 'username' not in session:
        return redirect('/login')

    # Haetaan thread tietokannasta
    query_thread = text("SELECT * FROM threads WHERE id = :thread_id")
    result_thread = db.session.execute(query_thread, {"thread_id": thread_id})
    thread = result_thread.fetchone()

    # Tarkista, onko käyttäjä threadin tekijä
    if session['username'] != thread.user_username:
        flash("Cant edit another users thread")
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Käsittele threadin muokkauslomakkeen tiedot tässä
        new_title = request.form['new_title']
        new_content = request.form['new_content']

        # Päivitä thread tietokantaan
        query_update_thread = text("UPDATE threads SET title = :new_title, content = :new_content WHERE id = :thread_id")
        db.session.execute(query_update_thread, {"new_title": new_title, "new_content": new_content, "thread_id": thread_id})
        db.session.commit()

        return redirect(url_for('index', thread_id=thread_id))

    # Renderöi muokkaussivu
    return render_template('edit_thread.html', thread=thread)

@app.route("/delete_thread/<int:thread_id>", methods=["GET","POST"])
def delete_thread(thread_id):
    username = session.get("username")

    if not username:
        flash("You must be logged in to delete a thread.", "error")
        return redirect("/login")

    # Hae thread
    query_thread = text("SELECT * FROM threads WHERE id = :thread_id")
    result_thread = db.session.execute(query_thread, {"thread_id": thread_id})
    selected_thread = result_thread.fetchone()

    if not selected_thread:
        flash("Thread not found.", "error")
        return redirect("/")

    # Tarkista, onko käyttäjä threadin tekijä
    if username != selected_thread.user_username:
        flash("You are not the author of this thread.", "error")
        return redirect("/")

    # Poista thread
    query_delete_thread = text("DELETE FROM threads WHERE id = :thread_id")
    db.session.execute(query_delete_thread, {"thread_id": thread_id})
    db.session.commit()

    flash("Thread deleted successfully.", "success")
    return redirect("/")
