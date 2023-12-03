from flask import render_template, redirect, session, flash, url_for
from sqlalchemy import text
from app import app
from db import db


def is_admin(username):
    query = text("SELECT is_admin FROM users WHERE username = :username")
    result = db.session.execute(query, {"username": username})
    is_admin = result.scalar()
    return is_admin == True

@app.route("/delete_thread/<int:thread_id>", methods=["GET", "POST"])
def admin_delete_thread(thread_id):
    # Check if the user is an admin
    username = session.get("username")
    if not is_admin(username):
        flash("You do not have permission to delete threads.", "error")
        return redirect("/")

@app.route("/delete_user/<int:user_id>", methods=["GET", "POST"])
def delete_user(user_id):
    # Check if user has logged in
    username = session.get("username")
    if not username:
        flash("You must be logged in to delete a user.", "error")
        return redirect("/login")

    # Check if the user is an admin
    if not is_admin(username):
        flash("You do not have permission to delete users.", "error")
        return redirect("/")

    # Get user
    query_user = text("SELECT * FROM users WHERE id = :user_id")
    result_user = db.session.execute(query_user, {"user_id": user_id})
    selected_user = result_user.fetchone()

    # Logging for debugging
    print(f"Admin: {is_admin(username)}")
    print(f"Selected User: {selected_user}")

    if not selected_user:
        flash("User not found.", "error")
        return redirect("/")

    # Delete user
    query_delete_user = text("DELETE FROM users WHERE id = :user_id")
    db.session.execute(query_delete_user, {"user_id": user_id})
    db.session.commit()

    flash("User deleted successfully.", "success")
    return redirect(url_for("admin_page"))

@app.route("/admin", methods=["GET"])
def admin_page():
    # Check if the current user is an admin
    username = session.get("username")
    if not is_admin(username):
        flash("You do not have permission to access this page.", "error")
        return redirect("/")

    # Modify the query for threads
    query_threads = text("SELECT * FROM threads")
    threads = db.session.execute(query_threads).fetchall()

    # Modify the query for users
    query_users = text("SELECT * FROM users")
    users = db.session.execute(query_users).fetchall()

    return render_template("admin_page.html", threads=threads, users=users)
