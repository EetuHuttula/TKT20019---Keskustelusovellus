CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    title VARCHAR(255)
);

CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);

