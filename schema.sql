DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL
)


DROP TABLE IF EXISTS recipes;
CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    notes TEXT,
    rating INTEGER,
    drink_name TEXT,
    drink_id INTEGER,
    drink_url TEXT,
    user_id INTEGER, 

    CONSTRAINT fk_user
    FOREIGN KEY (user_id)
      REFERENCES users(id)

)
