DROP TABLE if EXISTS groups CASCADE;
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

DROP TABLE if EXISTS students CASCADE;
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    id_group INTEGER REFERENCES groups(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

DROP TABLE if EXISTS teachers CASCADE;
CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
    
);

DROP TABLE if EXISTS subjects CASCADE;
CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    id_teacher INTEGER REFERENCES teachers(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
    
);

DROP TABLE if EXISTS grades CASCADE;
CREATE TABLE grades (
    id SERIAL PRIMARY KEY,
    id_student INTEGER REFERENCES students(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    id_subject INTEGER REFERENCES subjects(id)
    ON DELETE CASCADE
    ON UPDATE cascade,
    grade INTEGER CHECK (grade >= 0 and grade <=100),
    grade_date DATE NOT NULL
    
);

