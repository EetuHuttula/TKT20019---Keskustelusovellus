"""
app.py is used to lauch the application
"""
from os import getenv
from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
#importing modules
import routes
import users
import thread
import like
import prof
import threadpost

if __name__ == '__main__':
    #app updates after changes
    app.run(debug=True)
