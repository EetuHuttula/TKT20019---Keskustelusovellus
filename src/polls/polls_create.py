"""This module includes functions for getting
polls to polls page and answering to them"""
from flask import redirect, render_template, request, flash, session
from sqlalchemy import text
from app import app
from db import db
from src import secrets_token

@app.route("/polls", methods=["GET", "POST"])
def polls():
    # Fetch data about polls
    poll_query = text("""SELECT id, topic,user_username, created_at
                    FROM polls ORDER BY id DESC""")
    poll_result = db.session.execute(poll_query)
    polls_data = poll_result.fetchall()
    return render_template('polls.html', polls=polls_data)

@app.route("/create", methods=["POST"])
def create():
    username = session.get("username")

    if not username:
        flash("You must be logged in to make a poll.", "error")
        return redirect("/login")

    topic = request.form["topic"]
    choices = [
        request.form.get("choice1"),
        request.form.get("choice2"),
        request.form.get("choice3"),
        request.form.get("choice4")
    ]

    # Check if the topic is empty
    if not topic:
        flash("Topic cannot be empty", "error")
        return redirect("/polls")

    # Check if at least two choices are provided
    valid_choices = [choice for choice in choices if choice and any(c.isalpha() for c in choice)]
    if len(valid_choices) < 2:
        flash("At least two choices with at least two characters must be provided", "error")
        return redirect("/polls")

    # Insert a new poll into the 'polls' table
    insert_poll_query = text("""INSERT INTO polls (topic, created_at, user_username)
                            VALUES (:topic, NOW(), :user_username) RETURNING id""")
    poll_result = db.session.execute(insert_poll_query, {"topic": topic, "user_username": username})
    poll_id = poll_result.fetchone()[0]

    # Insert choices into the 'choices' table
    for choice in valid_choices:
        insert_choice_query = text(
            """INSERT INTO choices (poll_id, choice)
            VALUES (:poll_id, :choice)"""
        )
        db.session.execute(insert_choice_query, {"poll_id": poll_id, "choice": choice})

    db.session.commit()
    if request.method == "POST":
        csrf_token = request.form.get("csrf_token")
        if csrf_token != session.get("csrf_token"):
            flash("Invalid CSRF token. Please try again.")
            return render_template("polls.html")
    return redirect("/polls")
