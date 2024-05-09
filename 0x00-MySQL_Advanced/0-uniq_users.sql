-- Creates a table users with the following attributes:
-- id (integer, primary key, auto increment)
-- email (string, unique, never null, 255 characters)
-- name (string, 255 characters)
-- Will not fail if the table already exists

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
