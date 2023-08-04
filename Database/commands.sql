CREATE DATABASE swimming;

CREATE TABLE users (userID int NOT NULL AUTO_INCREMENT, email VARCHAR(200), passwords CHAR(77), PRIMARY KEY (userID)); -- passwords are SHA_256 hashes;

CREATE TABLE userDetails (userID int, name VARCHAR(200), city VARCHAR(200), state VARCHAR(200), pincode VARCHAR(200), gender VARCHAR(10), phone VARCHAR(10), FOREIGN KEY (userID) REFERENCES users(userID));

INSERT INTO users(userID, passwords) VALUES(%s, %s);

INSERT INTO userDetails (name, city, state, pincode, gender, phone) VALUES (%s, %s, %s, %s, %s, %s);

SELECT * FROM users;

-- FOREIGN KEY (userID) REFERENCES users(userID)
