-- Removed CREATE DATABASE line; CI runs against the provided database.
-- Use IF NOT EXISTS so applying the schema multiple times is safe.

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    creation_date VARCHAR(16) DEFAULT to_char(CURRENT_TIMESTAMP, 'DD.MM.YY')
);

CREATE TABLE IF NOT EXISTS threads (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    creation_date VARCHAR(16) DEFAULT to_char(CURRENT_TIMESTAMP, 'DD.MM.YY'),
    user_username VARCHAR(255) REFERENCES users(username) ON DELETE CASCADE NOT NULL,
    media_path JSONB
);

CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    post_date VARCHAR(16) DEFAULT to_char(CURRENT_TIMESTAMP, 'DD.MM.YY HH24:MI'),
    user_username VARCHAR(255) REFERENCES users (username) NOT NULL,
    thread_id INTEGER REFERENCES threads (id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE IF NOT EXISTS likes (
    id SERIAL PRIMARY KEY,
    user_username VARCHAR(255) REFERENCES users(username),
    thread_id INTEGER REFERENCES threads(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS polls (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    user_username VARCHAR(255) REFERENCES users (username) NOT NULL,
    created_at VARCHAR(16) DEFAULT to_char(CURRENT_TIMESTAMP, 'DD.MM.YY HH24:MI')
);

CREATE TABLE IF NOT EXISTS choices (
    id SERIAL PRIMARY KEY,
    poll_id INTEGER REFERENCES polls ON DELETE CASCADE,
    choice TEXT
);

CREATE TABLE IF NOT EXISTS answers (
    id SERIAL PRIMARY KEY,
    choice_id INTEGER REFERENCES choices ON DELETE CASCADE,
    poll_id INTEGER REFERENCES polls ON DELETE CASCADE,
    sent_at TIMESTAMP,
    user_username VARCHAR(255) REFERENCES users(username)
);