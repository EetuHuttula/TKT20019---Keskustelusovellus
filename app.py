from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text 
from os import getenv
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")

@app.route("/")
def index():
    query = text("SELECT * FROM threads")
    result = db.session.execute(query)
    threads = result.fetchall()
    return render_template('frontpage.html', threads=threads)

@app.route("/newthread")
def newthread():
    return render_template('newthread.html')


@app.route("/send", methods=["POST"])
def send():
    title = request.form["title"]
    content = request.form["content"]
    username = session.get("username")
      # Check if the user is logged in
    if not username:
        # Redirect to the login page or handle the case where the user is not logged in
        return redirect("/login")

    # Insert the message into the database with the associated username
    sql = text("INSERT INTO threads (title, content, user_username) VALUES (:title, :content, :user_username)")
    db.session.execute(sql, {"title": title, "content": content, "user_username": username})
    db.session.commit()

    return redirect("/")


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

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


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)