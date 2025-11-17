from sqlalchemy import text
import random
import string
import os
import sys
# Import db and app from root modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from db import db
from app import app

def reset_db():
  print(f"Clearing contents from all tables")
  # Delete in order of foreign key dependencies
  tables_to_clear = ['answers', 'choices', 'polls', 'likes', 'posts', 'threads', 'users']
  for table in tables_to_clear:
    try:
      sql = text(f"DELETE FROM {table}")
      db.session.execute(sql)
    except Exception as e:
      print(f"Could not clear {table}: {e}")
  db.session.commit()

def tables():
  """Returns all table names from the database except those ending with _id_seq"""
  sql = text(
    "SELECT table_name "
    "FROM information_schema.tables "
    "WHERE table_schema = 'public' "
    "AND table_name NOT LIKE '%_id_seq'"
  )
  
  result = db.session.execute(sql)
  return [row[0] for row in result.fetchall()]

def setup_db():
  """
    Creating the database
    If database tables already exist, those are dropped before the creation
  """
  tables_in_db = tables()
  if len(tables_in_db) > 0:
    print(f"Tables exist, dropping: {', '.join(tables_in_db)}")
    for table in tables_in_db:
      sql = text(f"DROP TABLE {table}")
      db.session.execute(sql)
    db.session.commit()

  print("Creating database")
  
  # Read schema from schema.sql file (or schematic.sql)
  schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schematic.sql')
  if not os.path.exists(schema_path):
    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schema.sql')
  
  with open(schema_path, 'r') as f:
    schema_sql = f.read().strip()
  
  sql = text(schema_sql)
  db.session.execute(sql)
  db.session.commit()

def create_test_data(amount: int = 50):
  print("Creating randomized test data.")
  
  # Create test users
  for i in range(min(10, amount)):
    username = f"testuser{i}"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    try:
      sql = text(f"INSERT INTO users (username, password) VALUES (:username, :password)")
      db.session.execute(sql, {"username": username, "password": password})
    except Exception as e:
      print(f"Could not create user {username}: {e}")
  
  # Create test threads
  for i in range(min(amount, 20)):
    title = f"Test Thread {i}: " + ''.join(random.choices(string.ascii_letters, k=20))
    content = ''.join(random.choices(string.ascii_letters + ' ', k=100))
    username = f"testuser{i % 10}"
    try:
      sql = text(f"INSERT INTO threads (title, content, user_username) VALUES (:title, :content, :username)")
      db.session.execute(sql, {"title": title, "content": content, "username": username})
    except Exception as e:
      print(f"Could not create thread: {e}")
  
  db.session.commit()
  print("Data creation complete.")

if __name__ == "__main__":
  with app.app_context():
    if len(sys.argv) > 1 and sys.argv[1] == "testdata":
      create_test_data()
    elif len(sys.argv) > 1 and sys.argv[1] == "setup":
      setup_db()
    elif len(sys.argv) > 1 and sys.argv[1] == "reset":
      reset_db()
    else:
      print("Use one of the following arguments: \n" \
            "   setup - Sets up the database \n" \
            "   reset - Resets the database \n" \
            "   testdata - Creates randomized data to the database \n")