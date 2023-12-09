"""
app.py is used to lauch the application
"""
from os import getenv
from flask import Flask
from src.secrets_token import generate_csrf_token

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
app.jinja_env.globals['csrf_token'] = generate_csrf_token
#importing modules
from src import routes
from src import users
from src import thread
from src import like
from src import profile_routes
from src import threadpost
from src import polls

if __name__ == '__main__':
    #app updates after changes
    app.run(debug=True)
