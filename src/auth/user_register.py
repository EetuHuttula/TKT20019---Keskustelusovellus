"""This module includes functions registration"""
from flask import redirect, render_template, request, session, flash
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from db import db
from app import app
from src import secrets_token
from src.auth.validate_registeration import validate_registration

# REGISTER function
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        csrf_token = request.form.get("csrf_token")
        if csrf_token != session.get("csrf_token"):
            flash("Invalid CSRF token. Please try again.")
            return render_template("register.html", username=request.form.get("username"))

        username = request.form.get("username")
        password = request.form.get("password")

        validation_errors = validate_registration(username, password)

        if validation_errors:
            for error in validation_errors:
                flash(error)
            return render_template("register.html", username=username)


        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Determine if the user should be an admin
        is_admin = username.lower() == "admin"

        # Save the user to the database
        try:
            sql = text("""INSERT INTO users (username, password, is_admin)
             VALUES (:username, :password, :is_admin)""")
            db.session.execute(sql, {"username": username,
                                     "password": hashed_password, "is_admin": is_admin})
            db.session.commit()

            session["username"] = username  # Automatically log in
            return redirect("/")

        except Exception as e:
            db.session.rollback()
            flash("Username already taken, please try again.", e)
            return render_template('register.html', username=username)
        finally:
            db.session.close()

    return render_template("register.html")
