from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text 
from os import getenv


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route("/")
def index():
    query = text("SELECT * FROM messages")
    result = db.session.execute(query)
    messages = result.fetchall()
    return render_template('frontpage.html', messages=messages)

@app.route("/newthread")
def newthread():
    return render_template('newthread.html')


@app.route("/send", methods=["POST"])
def send():
    title = request.form["title"]
    content = request.form["content"]
    sql = text("INSERT INTO messages (title, content) VALUES (:title, :content)")
    db.session.execute(sql, {"title": title, "content": content})
    db.session.commit()
    return redirect("/")


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    session["username"] = username
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)