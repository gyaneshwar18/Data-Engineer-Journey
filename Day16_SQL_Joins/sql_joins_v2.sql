----customers

CREATE TABLE customers (
    customer_id INT,
    name TEXT,
    city TEXT
);
INSERT INTO customers VALUES
(1,'Riya','Hyderabad'),
(2,'Aryan','Mumbai'),
(3,'Sneha','Delhi'),
(4,'Rahul','Pune');

---orders

CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    amount INT
);
 INSERT INTO orders VALUES
(101,1,500),
(102,1,700),
(103,2,300),
(104,5,900);
