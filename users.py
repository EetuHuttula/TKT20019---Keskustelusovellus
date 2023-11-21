from db import db
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from sqlalchemy import text 
from sqlalchemy.exc import SQLAlchemyError

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Handle the login logic for POST requests
        username = request.form["username"]
        password = request.form["password"]

        # Validate username and password
        try:
            query = text("SELECT id, password FROM users WHERE username=:username")
            result = db.session.execute(query, {"username": username})
            user = result.fetchone()

            if not user:
                # TODO: Handle invalid username
                return redirect("/")

            stored_hashed_password = user.password

            if check_password_hash(stored_hashed_password, password):
                # Password is correct
                session["username"] = username
                return redirect("/")
            else:
                # Invalid password
                return redirect("/")

        except SQLAlchemyError as e:
            # Handle the database error, log it, or provide a user-friendly message
            db.session.rollback()
            print(f"Database Error: {str(e)}")
            return redirect("/")
        finally:
            db.session.close()    
    else:
        # Handle the rendering of the login form for GET requests
        return render_template('login.html')

#REGISTER function

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Tallenna käyttäjä tietokantaan
        try:
            sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
            db.session.execute(sql, {"username": username, "password": hashed_password})
            db.session.commit()

            session["username"] = username  # Kirjaudu sisään automaattisesti
            return redirect("/")

        except Exception as e:
            db.session.rollback()
            print(f"Registration Error: {str(e)}")
            return render_template('registration_failed.html')

        finally:
            db.session.close()

    else:
        return render_template('register.html')

#LOGOUT function

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")