CREATE TABLE movie (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    name VARCHAR(40) NOT NULL, 
    picture VARCHAR(30), 
    info VARCHAR(500), 
    actors VARCHAR(200), 
    duration VARCHAR(20) NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE user (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    username VARCHAR(30) NOT NULL, 
    firstname VARCHAR(35) NOT NULL, 
    lastname VARCHAR(35) NOT NULL, 
    email VARCHAR(40) NOT NULL, 
    password_hash VARCHAR(240) NOT NULL, 
    phone_number VARCHAR(25), 
    photo VARCHAR(50), 
    PRIMARY KEY (id), 
    UNIQUE (email), 
    UNIQUE (username)
);

CREATE TABLE movie_schedule (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    date VARCHAR(20) NOT NULL, 
    time VARCHAR(20) NOT NULL, 
    movie_id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(movie_id) REFERENCES movie (id)
);

CREATE TABLE reservation (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    date VARCHAR(20) NOT NULL, 
    time VARCHAR(20) NOT NULL, 
    movie_id INTEGER NOT NULL, 
    user_id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(movie_id) REFERENCES movie (id), 
    FOREIGN KEY(user_id) REFERENCES user (id)
);

