CREATE TABLE students(
	dep varchar(45), 
	course varchar(45), 
	year varchar(45), 
	semester varchar(45), 
	sid int,  
	sname varchar(45), 
	reg varchar(45), 
	roll varchar(45), 
	gender varchar(45), 
	dob varchar(45), 
	email varchar(45), 
	phone varchar(45), 
	address varchar(45), 
	teacher varchar(45),
    sgpa VARCHAR(45)
);

CREATE TABLE admin1(
	user_name VARCHAR(100),
    pass_word VARCHAR(100),
    email1 VARCHAR(100),
    PRIMARY KEY(user_name)
);

CREATE TABLE student1(
	stud_id INTEGER,
    email1 VARCHAR(100),
    stud_password VARCHAR(100),
    PRIMARY KEY(stud_id)
);

DROP TABLE students;
DROP TABLE admin1;
DROP TABLE student1;

TRUNCATE TABLE students;
TRUNCATE TABLE admin1;
TRUNCATE TABLE student1;

SET SQL_SAFE_UPDATES = 0;
DELETE FROM student1 where stud_id = 2;
UPDATE students SET sgpa = 8.0 where sid=1 and semester="SEM-2";

SELECT * FROM students;
SELECT * FROM admin1;
SELECT * FROM student1;







