from flask import Flask, redirect, render_template, request, session, send_file, url_for
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


@app.route("/newthread", methods=["GET", "POST"])
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

    return render_template('newthread.html')

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

#LOGIN function

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


if __name__ == '__main__':
    app.run(debug=True)