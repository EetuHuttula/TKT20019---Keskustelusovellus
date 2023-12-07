"""This module includes functions for getting
polls to polls page and answering to them"""
from flask import redirect, render_template, request, flash, session
from sqlalchemy import text
from app import app
from db import db
from src import delete_polls

@app.route("/polls", methods=["GET", "POST"])
def polls():
    # Fetch data about polls
    poll_query = text("""SELECT id, topic,user_username, created_at
                    FROM polls ORDER BY id DESC""")
    poll_result = db.session.execute(poll_query)
    polls_data = poll_result.fetchall()
    return render_template('polls.html', polls=polls_data)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    username = session.get("username")

    if not username:
        flash("You must be logged in to make a poll.", "error")
        return redirect("/login")

    topic = request.form["topic"]
    choices = [request.form.get('choice1'), request.form.get('choice2'), request.form.get('choice3'), request.form.get('choice4')]

    # Check if the topic is empty
    if not topic:
        flash("Topic cannot be empty", "error")
        return redirect("/polls")

    # Check if at least two choices are provided
    if len(choices) < 2 or all(not choice.strip() for choice in choices):
            flash("At least two non-empty choices must be provided", "error")
            return redirect("polls")

    # Insert a new poll into the 'polls' table
    insert_poll_query = text("""INSERT INTO polls (topic, created_at, user_username)
                            VALUES (:topic, NOW(), :user_username) RETURNING id""")
    poll_result = db.session.execute(insert_poll_query, {"topic": topic, "user_username": username})
    poll_id = poll_result.fetchone()[0]

    # Insert choices into the 'choices' table
    choices = request.form.getlist("choice")
    for choice in choices:
        if choice != "":
            insert_choice_query = text("""INSERT INTO choices (poll_id, choice)
                                        VALUES (:poll_id, :choice)""")
            db.session.execute(insert_choice_query, {"poll_id": poll_id, "choice": choice})

    db.session.commit()
    return redirect("/polls")


@app.route("/poll/<int:poll_id>")
def poll(poll_id):
    query_topic = text("SELECT topic FROM polls WHERE id=:poll_id")
    result_topic = db.session.execute(query_topic, {"poll_id": poll_id})
    topic = result_topic.fetchone()[0]

    query_choices = text("SELECT id, choice FROM choices WHERE poll_id=:poll_id")
    result_choices = db.session.execute(query_choices, {"poll_id": poll_id})
    choices = result_choices.fetchall()
    return render_template("poll.html", poll_id=poll_id, topic=topic, choices=choices)

@app.route("/answer", methods=["POST"])
def answer():
    poll_id = request.form["id"]
    if "answer" in request.form:
        choice_id = request.form["answer"]
        answer_query = text("INSERT INTO answers (choice_id, sent_at) VALUES (:choice_id, NOW())")
        db.session.execute(answer_query, {"choice_id": choice_id})
        db.session.commit()
    return redirect("/result/" + str(poll_id))

@app.route("/result/<int:poll_id>")
def result(poll_id):
    query_topic = text("SELECT topic FROM polls WHERE id=:poll_id")
    result_topic = db.session.execute(query_topic, {"poll_id": poll_id})
    topic = result_topic.fetchone()[0]

    query_choices = text("SELECT c.choice, COUNT(a.id) FROM choices c "
                        "LEFT JOIN answers a ON c.id=a.choice_id "
                        "WHERE c.poll_id=:poll_id GROUP BY c.id")
    result_choices = db.session.execute(query_choices, {"poll_id": poll_id})
    choices = result_choices.fetchall()

    return render_template("result.html", topic=topic, choices=choices)
