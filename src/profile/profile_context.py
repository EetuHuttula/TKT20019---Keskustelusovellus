from sqlalchemy import text
from db import db

# Function to retrieve user information from the database
def get_user_info(username):
    query = text("""SELECT id, username, creation_date 
    FROM users WHERE username=:username""")
    result = db.session.execute(query, {"username": username})
    user = result.fetchone()
    return user

# Function to get thread count for a user
def get_thread_count(username):
    query = text("""SELECT COUNT(id) 
    FROM threads WHERE user_username=:username""")
    result = db.session.execute(query, {"username": username})
    thread_count = result.scalar()  # scalar() fetches the count value
    return thread_count

# Function to get post count for a user
def get_post_count(username):
    query = text("""SELECT COUNT(id)
    FROM posts WHERE user_username=:username""")
    result = db.session.execute(query, {"username": username})
    post_count = result.scalar()  # scalar() fetches the count value
    return post_count

def get_like_count(username):
    query = text("""SELECT COUNT(id)
    FROM likes WHERE user_username=:username""")
    result = db.session.execute(query, {"username": username})
    like_count = result.scalar()
    return like_count

def get_poll_count(username):
    query = text("""SELECT COUNT(id)
    FROM polls WHERE user_username=:username""")
    result = db.session.execute(query, {"username": username})
    poll_count = result.scalar()
    return poll_count
