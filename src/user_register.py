"""This module includes functions registration"""
from flask import redirect, render_template, request, session, flash
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from db import db
from app import app
from src import secrets_token
import re

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

        if not username.strip():
            flash("Username cannot be empty. Please try again.")
            return render_template('register.html', username=username)

        if not password:
            flash("Please provide a password.")
            return render_template('register.html', username=username)

        if not username or not password:
            flash("Please provide both username and password")
            return render_template('register.html', username=username)

        if len(password) < 8:
            flash("Password must be at least 8 characters long.")
            return render_template('register.html', username=username)

        if not re.search("[a-zA-Z]", password):
            flash("Password must contain at least one letter.")
            return render_template('register.html', username=username)

        if not re.search("[0-9]", password):
            flash("Password must contain at least one digit.")
            return render_template('register.html', username=username)

        if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
            flash("Password must contain at least one special character.")
            return render_template('register.html', username=username)

        if ' ' in password:
            flash("Password cannot contain whitespaces.")
            return render_template('register.html', username=username)

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
            flash("Username already taken, please try again")
            return render_template('register.html', username=username)
        finally:
            db.session.close()

    return render_template('register.html')