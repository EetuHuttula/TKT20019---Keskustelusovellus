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
from src.auth import user_login, user_register
from src.threads import thread_view, thread_create_reply, thread_management, thread_like 
from src.polls import polls_create, polls_delete, polls_view_answer
from src.profile import profile_routes

if __name__ == '__main__':
    #app updates after changes
    app.run(debug=True)
