"""
app.py is used to lauch the application
"""
from os import getenv
from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
#importing modules
from src import routes
from src import users
from src import thread
from src import like
from src import prof
from src import threadpost
from src import polls

if __name__ == '__main__':
    #app updates after changes
    app.run(debug=True)
