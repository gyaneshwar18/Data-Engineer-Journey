CREATE TABLE employees (
    emp_id INT,
    name TEXT,
    department TEXT,
    salary INT,
    city TEXT
);

INSERT INTO employees VALUES
(1,'Riya','Data',60000,'Hyderabad'),
(2,'Aryan','IT',50000,'Mumbai'),
(3,'Sneha','Data',75000,'Hyderabad'),
(4,'Rahul','HR',45000,'Delhi'),
(5,'Neha','IT',70000,'Mumbai');

SELECT * FROM employees;

SELECT name, salary
FROM employees
WHERE salary > 60000;

SELECT *
FROM employees
ORDER BY salary DESC;


