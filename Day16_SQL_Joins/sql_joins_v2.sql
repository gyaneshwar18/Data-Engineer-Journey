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
INSERT INTO orders VALUES
(101,1,500),
(102,1,700),
(103,2,300),
(104,5,900);

SELECT c.name, o.amount
FROM customers c
INNER JOIN orders o
ON c.customer_id = o.customer_id;

# LEFT JOIN

SELECT c.name, o.amount
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id;

# Find Customers Without Orders
Select c.name
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

# Find Customers Without Orders

SELECT c.name,
       o.amount AS total_spend
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY c.name;
