from flask import redirect, render_template, request, flash, session
from sqlalchemy import text
from app import app
from db import db

@app.route("/poll/<int:poll_id>")
def poll(poll_id):

    username = session.get("username")
    if not username:
        flash("You must be logged in to view a poll.", "error")
        return redirect("/login")

    query_topic = text("SELECT topic FROM polls WHERE id=:poll_id")
    result_topic = db.session.execute(query_topic, {"poll_id": poll_id})
    topic = result_topic.fetchone()[0]

    query_choices = text("SELECT id, choice FROM choices WHERE poll_id=:poll_id")
    result_choices = db.session.execute(query_choices, {"poll_id": poll_id})
    choices = result_choices.fetchall()
    return render_template("poll.html", poll_id=poll_id, topic=topic, choices=choices)

@app.route("/answer", methods=["POST"])
def answer():

    username = session.get("username")

    if not username:
        flash("You must be logged in to answer a poll.", "error")
        return redirect("/login")

    poll_id = request.form["id"]
    if "answer" in request.form:
        choice_id = request.form["answer"]
        answer_query = text("""INSERT INTO answers
        (choice_id, sent_at) VALUES (:choice_id, NOW())""")
        db.session.execute(answer_query, {"choice_id": choice_id})
        db.session.commit()
    return redirect("/result/" + str(poll_id))

@app.route("/result/<int:poll_id>")
def result(poll_id):

    username = session.get("username")
    if not username:
        flash("You must be logged in to see the results of the poll.", "error")
        return redirect("/login")
    query_topic = text("SELECT topic FROM polls WHERE id=:poll_id")
    result_topic = db.session.execute(query_topic, {"poll_id": poll_id})
    topic = result_topic.fetchone()[0]
    query_choices = text(
    "SELECT c.choice, COUNT(a.id) FROM choices c "
    "LEFT JOIN answers a ON c.id=a.choice_id "
    "WHERE c.poll_id=:poll_id GROUP BY c.id")
    result_choices = db.session.execute(query_choices, {"poll_id": poll_id})
    choices = result_choices.fetchall()
    return render_template("result.html", topic=topic, choices=choices)
