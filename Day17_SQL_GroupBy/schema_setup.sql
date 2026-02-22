-- =====================================
-- Day 17: Schema Setup for GROUP BY
-- =====================================

-- Drop tables if they exist (safe rerun)
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;

-- Create customers table
CREATE TABLE customers (
    customer_id INT,
    name TEXT,
    city TEXT
);

-- Insert sample customers
INSERT INTO customers VALUES
(1,'Riya','Hyderabad'),
(2,'Aryan','Mumbai'),
(3,'Sneha','Delhi'),
(4,'Rahul','Pune');


-- Create orders table
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    amount INT
);

-- Insert sample orders
INSERT INTO orders VALUES
(101,1,500),
(102,1,700),
(103,2,300),
(104,2,400),
(105,3,900),
(106,5,1200);  -- No matching customer (for join practice)

-- 1️⃣ Total order amount per customer
SELECT customer_id,
       SUM(amount) AS total_spend
FROM orders
GROUP BY customer_id;

--2️⃣ Number of orders per customer

SELECT customer_id,
       COUNT(order_id) AS total_orders
FROM orders
GROUP BY customer_id;

--3️⃣ Average order value per customer

select customer_id,
        AVG(amount) AS AVG_ORDER
FROM orders
GROUP BY customer_id;

---- 4️⃣ Customers who spent more than 1000

SELECT customer_id,
       SUM(amount) AS total_spend
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 1000;

---- 5️⃣ Total spend per customer name (JOIN + GROUP BY)

SELECT c.name, SUM(o.amount) AS TOTAL_SPEND
from customers c
join orders o
on c.customer_id=o.customer_id
GROUP BY c.name;




