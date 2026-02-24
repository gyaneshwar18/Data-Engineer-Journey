------1️⃣ Customers who spent more than average order amount
SELECT customer_id, amount
FROM orders
WHERE amount > (
    SELECT AVG(amount)
    FROM orders
);

--- 2️⃣ Customers who placed orders (using IN)

select name
from customers
where customer_id in (select customer_id from orders);


--3️⃣ Highest spender (subquery in WHERE)

select *
from orders 
where amount =(select max(amount) from orders);

---- Total spend per customer using subquery

SELECT *
FROM (
    SELECT customer_id,
           SUM(amount) AS total_spend
    FROM orders
    GROUP BY customer_id
) AS summary
WHERE total_spend > 800;