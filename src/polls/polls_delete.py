"""This module includes function for deleting polls"""
from flask import redirect, flash, session
from sqlalchemy import text
from app import app
from db import db

@app.route("/delete_poll/<int:poll_id>", methods=["GET"])
def delete_poll(poll_id):
    username = session.get("username")

    if not username:
        flash("You must be logged in to delete a poll.", "error")
        return redirect("/login")

    # Check if the user is the owner of the poll
    check_owner_query = text("""SELECT user_username
                    FROM polls WHERE id = :poll_id""")
    owner_result = db.session.execute(check_owner_query, {"poll_id": poll_id})
    owner_username = owner_result.fetchone()

    if not owner_username or owner_username[0] != username:
        flash("You do not have permission to delete this poll.", "error")
        return redirect("/polls")

    # Delete the poll and associated choices
    delete_choices_query = text("DELETE FROM choices WHERE poll_id = :poll_id")
    db.session.execute(delete_choices_query, {"poll_id": poll_id})

    delete_poll_query = text("DELETE FROM polls WHERE id = :poll_id")
    db.session.execute(delete_poll_query, {"poll_id": poll_id})

    db.session.commit()
    flash("Poll successfully deleted.", "success")
    return redirect("/polls")
