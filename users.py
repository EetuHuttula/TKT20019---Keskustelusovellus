"""This module includes functions for login and registration"""
from flask import redirect, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from db import db
from app import app

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Handle the login logic for POST requests
        username = request.form["username"]
        password = request.form["password"]
        if not username or not password:
            flash("Please provide both username and password")
            return render_template('login.html')

        # Validate username and password
        try:
            query = text("SELECT id, password FROM users WHERE username=:username")
            result = db.session.execute(query, {"username": username})
            user = result.fetchone()

            if not user:
                flash("Invalid username or password")
                return redirect("/login")

            stored_hashed_password = user.password

            if check_password_hash(stored_hashed_password, password):
                # Password is correct
                session["username"] = username
                return redirect("/")
                # Invalid password
            flash("Invalid username or password")
            return redirect("/login.html")

        except SQLAlchemyError as e:
            # Handle the database error, log it, or provide a user-friendly message
            db.session.rollback()
            print(f"Database Error: {str(e)}")
            return redirect("/")
        finally:
            db.session.close()

    return render_template('login.html')

#REGISTER function
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please provide both username and password")
            return render_template('register.html')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Save the user to the database
        try:
            sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
            db.session.execute(sql, {"username": username, "password": hashed_password})
            db.session.commit()

            session["username"] = username  # Automatically log in
            return redirect("/")

        except Exception as e:
            db.session.rollback()
            flash("Username taken")
            return render_template('/register.html')
        finally:
            db.session.close()
    return render_template('register.html')

#LOGOUT function
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")
