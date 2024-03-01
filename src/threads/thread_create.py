from flask import redirect, request, session, url_for, flash
from werkzeug.utils import secure_filename
from sqlalchemy import text
from app import app
from db import db
import os, json

@app.route("/send", methods=["POST"])
def send():
    if request.method == "POST":
        csrf_token = request.form.get("csrf_token")
        if csrf_token != session.get("csrf_token"):
            flash("Invalid CSRF token. Please try again.")
            return redirect(url_for("index"))

        # Validate user input (improved)
        title = request.form.get("title", "").strip()  # Handle missing input gracefully
        content = request.form.get("content", "").strip()  # Handle missing input gracefully
        if not title or not content:
            flash("Title or message can't be empty. Please try again.")
            return redirect(url_for("index"))

        # Securely handle media uploads (improved error handling)
        media_paths = []
        image = request.files.get('image')
        video = request.files.get('video')
        if image:
            try:
                image_filename = secure_filename(image.filename)
                image_path = os.path.join('static/uploads', image_filename)
                image.save(image_path)
                media_paths.append(image_path)
            except Exception as e:
                flash(f"Error uploading image: {e}")
                return redirect(url_for("index"))

        if video:
            try:
                video_filename = secure_filename(video.filename)
                video_path = os.path.join('static/uploads', video_filename)
                video.save(video_path)
                media_paths.append(video_path)
            except Exception as e:
                flash(f"Error uploading video: {e}")
                return redirect(url_for("index"))

        # Ensure user is logged in
        username = session.get("username")
        if not username:
            return redirect("/login")

        # Prepare and execute database insertion (concise & improved)
        
        try:
            media_paths_json = json.dumps(media_paths) if media_paths else None  # Handle empty list
            db.session.execute(text("""
                INSERT INTO threads (title, content, user_username, media_path)
                VALUES (:title, :content, :user_username, :media_path)
            """), {
                "title": title,
                "content": content,
                "user_username": username,
                "media_path": media_paths_json
            })
            db.session.commit()
            return redirect("/")
        except Exception as e:
            flash(f"Error saving data: {e}")
            return redirect(url_for("index"))  # Redirect back to the form on error

    # Handle other HTTP methods (unchanged)
    return redirect("/")