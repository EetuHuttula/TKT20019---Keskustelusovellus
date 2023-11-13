from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('frontpage.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/login")
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)