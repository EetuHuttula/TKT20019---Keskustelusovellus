CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    user_username VARCHAR(255) REFERENCES users(username) NOT NULL
);

ALTER TABLE messages
ALTER COLUMN user_id TYPE VARCHAR(255);



