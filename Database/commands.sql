CREATE DATABASE swimming;

CREATE TABLE users (userID int NOT NULL AUTO_INCREMENT, email VARCHAR(200), passwords CHAR(77), PRIMARY KEY (userID)); -- passwords are SHA_256 hashes;

CREATE TABLE userDetails (userID int, name VARCHAR(200), city VARCHAR(200), state VARCHAR(200), pincode VARCHAR(200), gender VARCHAR(10), phone VARCHAR(10), FOREIGN KEY (userID) REFERENCES users(userID));

INSERT INTO users(userID, passwords) VALUES(%s, %s);

INSERT INTO userDetails (name, city, state, pincode, gender, phone) VALUES (%s, %s, %s, %s, %s, %s);

SELECT * FROM users;

-- FOREIGN KEY (userID) REFERENCES users(userID)


CREATE TABLE admin (adminID int NOT NULL AUTO_INCREMENT, email VARCHAR(200), passwords CHAR(77), PRIMARY KEY (adminID));

INSERT INTO admin(email, passwords) VALUES( 'admin@test.com', '$5$rounds=535000$FlCrGe1gXPGjJTmZ$bw2C0nr2mX6uCgJBems6EG23siqYOfNO9mmoHu/oL6/' );

INSERT INTO userDetails (name, city, state, pincode, gender, phone) VALUES ('Testuser2', 'Testuser2', 'Testuser2', '123456', 'Male', '7894561230');


UPDATE userDetails 
SET userID = 2
WHERE Name = 'Testuser2';






Post Gres Commands:
CREATE TABLE users (user_id SERIAL PRIMARY KEY, name VARCHAR(200), dob DATE, Phone CHAR(10),address VARCHAR(300), address2  VARCHAR(300), state  VARCHAR(20), country  VARCHAR(40), pincode VARCHAR(6), roleID SERIAL);

CREATE TABLE login (user_id INT, email VARCHAR(200), password CHAR(77), FOREIGN KEY (user_id) REFERENCES users(user_id));

CREATE TABLE permission (permission_id SERIAL PRIMARY KEY, Description VARCHAR(200));

CREATE TABLE role (roleID SERIAL PRIMARY KEY, Description VARCHAR(200));

CREATE TABLE role_perm (roleID INT REFERENCES role(roleID), FOREIGN KEY permission_id INT REFERENCES permission(permission_id));

CREATE TABLE membership (user_id INT REFERENCES users(user_id),  membershipStatus BOOLEAN DEFAULT FALSE, payment_id INT REFERENCES payment(payment_id), membership_start DATE, membership_end DATE );

CREATE TABLE payment (payment_id SERIAL PRIMARY KEY, paymentStatus BOOLEAN DEFAULT FALSE, transactionId VARCHAR(200));

CREATE TABLE competition (competition_id SERIAL PRIMARY KEY, name VARCHAR(200), location VARCHAR(100), startdate DATE, enddate DATE);

CREATE TABLE team (team_id SERIAL PRIMARY KEY, name VARCHAR(50), Description VARCHAR(65530));

CREATE TABLE team_member (team_id INT REFERENCES team(team_id), member_id INT users(user_id));

CREATE TABLE competition_team(competition_id INT REFERENCES competition(competition_id), team_id INT REFERENCES team(team_id));

CREATE TABLE competition_member(competition_id INT REFERENCES competition(competition_id), user_id INT REFERENCES user_id(user_id));

CREATE TABLE athlete (user_id INT REFERENCES users(user_id), skillLevel VARCHAR(200), progressNotes VARCHAR(65530), event VARCHAR(100), timings DATE , eventDate DATE);

CREATE TABLE equipment (equipment_id SERIAL PRIMARY KEY, name VARCHAR(100), quanitiy INT, location VARCHAR(100));




GRANT ALL PRIVILEGES ON DATABASE swimming to flask;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO flask;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public to flask;
