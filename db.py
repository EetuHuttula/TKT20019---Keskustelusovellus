"""This module is for db connection"""
from os import getenv
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, inspect

# Initialize SQLAlchemy without an app to avoid circular imports
db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the Flask app"""
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    
    # Create all tables from the schema SQL file
    with app.app_context():
        try:
            # Find schematic.sql in the project root
            schema_path = Path(__file__).parent / 'schematic.sql'
            
            if schema_path.exists():
                with open(schema_path, 'r') as f:
                    sql_script = f.read()
                    # Split by semicolon and execute each statement
                    for statement in sql_script.split(';'):
                        statement = statement.strip()
                        # Skip CREATE DATABASE statements and empty statements
                        if statement and not statement.upper().startswith('CREATE DATABASE'):
                            try:
                                db.session.execute(text(statement))
                            except Exception as e:
                                # Table might already exist, continue
                                pass
                    db.session.commit()
        except Exception as e:
            # Database might already be initialized or schema file not found
            try:
                db.session.rollback()
            except:
                pass
