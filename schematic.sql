CREATE DATABASE porinanurkka;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    creation_date VARCHAR(16) DEFAULT to_char(CURRENT_TIMESTAMP, 'DD.MM.YY')
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    creation_date VARCHAR(16) DEFAULT to_char(CURRENT_TIMESTAMP, 'DD.MM.YY'),
    user_username VARCHAR(255) REFERENCES users(username) ON DELETE CASCADE NOT NULL
);


CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    post_date VARCHAR(16) DEFAULT to_char(CURRENT_TIMESTAMP, 'DD.MM.YY'),
    user_username VARCHAR(255) REFERENCES users (username) NOT NULL,
    thread_id INTEGER REFERENCES threads (id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    user_username VARCHAR(255) REFERENCES users(username),
    thread_id INTEGER REFERENCES threads(id) ON DELETE CASCADE
);

CREATE TABLE polls (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    user_username VARCHAR(255) REFERENCES users (username) NOT NULL,
    created_at TIMESTAMP
);

CREATE TABLE choices (
    id SERIAL PRIMARY KEY,
    poll_id INTEGER REFERENCES polls,
    choice TEXT
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    choice_id INTEGER REFERENCES choices,
    sent_at TIMESTAMP
);