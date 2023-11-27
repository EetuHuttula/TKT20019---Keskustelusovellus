from app import app
from flask import redirect, render_template, request, session, url_for, flash
from db import db
from sqlalchemy import text 

@app.route("/", methods=["GET", "POST"])
def index():
    query = text("""
        SELECT t.*, COUNT(l.id) AS like_count
        FROM threads t
        LEFT JOIN likes l ON t.id = l.thread_id
        GROUP BY t.id
    """)
    result = db.session.execute(query)
    threads = result.fetchall()
    return render_template('frontpage.html', threads=threads)

def newthread():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        username = session.get("username")

        if not username:
            return redirect(url_for("login"))

        thread = thread(title=title, content=content, user_username=username)
        db.session.add(thread)
        db.session.commit()

        return redirect(url_for("index"))

@app.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    if request.method == 'GET':
        # Fetch the thread and its posts using direct SQL queries
        query_thread = text("SELECT * FROM threads WHERE id = :thread_id")
        result_thread = db.session.execute(query_thread, {"thread_id": thread_id})
        selected_thread = result_thread.fetchone()

        query_posts = text("SELECT * FROM posts WHERE thread_id = :thread_id")
        result_posts = db.session.execute(query_posts, {"thread_id": thread_id})
        posts = result_posts.fetchall()

        return render_template('view_thread.html', thread=selected_thread, posts=posts)

    elif request.method == 'POST':
        # Handle the form submission for posting a reply
        content = request.form['content']
        username = session.get('username')

        if not username:
            # Redirect to login or handle the case where the user is not logged in
            return redirect('/login')

        # Insert the reply into the posts table using direct SQL query
        query_insert_post = text("INSERT INTO posts (content, user_username, thread_id) VALUES (:content, :username, :thread_id)")
        db.session.execute(query_insert_post, {"content": content, "username": username, "thread_id": thread_id})
        db.session.commit()

        return redirect(url_for('view_thread', thread_id=thread_id))

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
    if 'username' not in session:
        return redirect('/login')  # Redirect to login if not logged in

    username = session['username']
    user = get_user_info(username)

    if user:
        # Fetch thread count for the user
        thread_count = get_thread_count(user.username)

        # Fetch post count for the user
        post_count = get_post_count(user.username)

        return render_template('profile.html', thread_count=thread_count, post_count=post_count, user=user)
    else:
        # Handle the case when the user is not found
        return render_template('profile.html', thread_count=0, post_count=0, user=None)

# Function to retrieve user information from the database
def get_user_info(username):
    query = text("SELECT * FROM users WHERE username=:username")
    result = db.session.execute(query, {"username": username})
    user = result.fetchone()
    return user

# Function to get thread count for a user
def get_thread_count(username):
    query = text("SELECT COUNT(*) FROM threads WHERE user_username=:username")
    result = db.session.execute(query, {"username": username})
    thread_count = result.scalar()  # scalar() fetches the count value
    return thread_count

# Function to get post count for a user
def get_post_count(username):
    query = text("SELECT COUNT(*) FROM posts WHERE user_username=:username")
    result = db.session.execute(query, {"username": username})
    post_count = result.scalar()  # scalar() fetches the count value
    return post_count

@app.route("/like/<int:thread_id>", methods=["POST"])
def like(thread_id):
    username = session.get("username")

    if not username:
        flash("You must be logged in to like a thread.", "error")
        return redirect("/login")

    # Check if the user has already liked the thread
    query_existing_like = text("SELECT * FROM likes WHERE user_username = :username AND thread_id = :thread_id")
    result_existing_like = db.session.execute(query_existing_like, {"username": username, "thread_id": thread_id})
    existing_like = result_existing_like.fetchone()

    if existing_like:
        flash("You have already liked this thread.", "error")
    else:
        # Add a new like
        query_new_like = text("INSERT INTO likes (user_username, thread_id) VALUES (:username, :thread_id)")
        db.session.execute(query_new_like, {"username": username, "thread_id": thread_id})
        db.session.commit()
        flash("You liked the thread!", "success")
    return redirect(url_for("index"))
