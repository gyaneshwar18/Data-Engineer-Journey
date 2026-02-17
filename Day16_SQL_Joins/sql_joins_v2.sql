CREATE TABLE IF NOT EXISTS customers (
    customer_id INT,
    name TEXT,
    city TEXT
);
INSERT INTO customers VALUES
(1,'Riya','Hyderabad'),
(2,'Aryan','Mumbai'),
(3,'Sneha','Hyderabad'),
(4,'Rahul','Delhi'),
(5,'Neha','Mumbai');

CREATE TABLE IF NOT EXISTS orders (
    order_id INT,
    customer_id INT,
    amount INT
);
