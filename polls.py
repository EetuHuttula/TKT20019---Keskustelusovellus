"""This module includes functions for getting
polls to polls page and answering to them"""
from flask import redirect, render_template, request, flash, session
from sqlalchemy import text
from app import app
from db import db

@app.route("/polls", methods=["GET", "POST"])
def polls():
    # Fetch data about polls
    poll_query = text("SELECT id, topic,user_username, created_at FROM polls ORDER BY id DESC")
    poll_result = db.session.execute(poll_query)
    polls = poll_result.fetchall()
    return render_template('polls.html', polls=polls)

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
    choices = request.form["choice"]
    
    # Check if the topic is empty
    if not topic:
        flash("Topic cannot be empty", "error")
        return redirect("/polls")
    
     # Check if there is at least one choice
    if len(choices) < 2 or all(choice == "" for choice in choices):
        flash("At least two choices must be provided", "error")
        return redirect("/polls")
   
    # Insert a new poll into the 'polls' table
    insert_poll_query = text("INSERT INTO polls (topic, created_at, user_username) VALUES (:topic, NOW(), :user_username) RETURNING id")
    poll_result = db.session.execute(insert_poll_query, {"topic": topic, "user_username": username})
    poll_id = poll_result.fetchone()[0]

     # Fetch user information
    user_query = text("SELECT username FROM users WHERE username = :username")
    user_result = db.session.execute(user_query, {"username": username})
    user = user_result.fetchone()
    
    # Insert choices into the 'choices' table
    choices = request.form.getlist("choice")
    for choice in choices:
        if choice != "":
            insert_choice_query = text("INSERT INTO choices (poll_id, choice) VALUES (:poll_id, :choice)")
            db.session.execute(insert_choice_query, {"poll_id": poll_id, "choice": choice})

    db.session.commit()
    return redirect("/polls")


@app.route("/poll/<int:id>")
def poll(id):
    query = text("SELECT topic FROM polls WHERE id=:id")
    result = db.session.execute(query, {"id":id})
    topic = result.fetchone()[0]
    query1 = text("SELECT id, choice FROM choices WHERE poll_id=:id")
    result = db.session.execute(query1, {"id":id})
    choices = result.fetchall()
    return render_template("poll.html", id=id, topic=topic, choices=choices)

@app.route("/answer", methods=["POST"])
def answer():
    poll_id = request.form["id"]
    if "answer" in request.form:
        choice_id = request.form["answer"]
        query = text("INSERT INTO answers (choice_id, sent_at) VALUES (:choice_id, NOW())")
        db.session.execute(query, {"choice_id":choice_id})
        db.session.commit()
    return redirect("/result/" + str(poll_id))

@app.route("/result/<int:id>")
def result(id):
    query = text("SELECT topic FROM polls WHERE id=:id")
    result = db.session.execute(query, {"id":id})
    topic = result.fetchone()[0]
    query1 = text("SELECT c.choice, COUNT(a.id) FROM choices c LEFT JOIN answers a " \
          "ON c.id=a.choice_id WHERE c.poll_id=:poll_id GROUP BY c.id")
    result = db.session.execute(query1, {"poll_id":id})
    choices = result.fetchall()
    return render_template("result.html", topic=topic, choices=choices)
