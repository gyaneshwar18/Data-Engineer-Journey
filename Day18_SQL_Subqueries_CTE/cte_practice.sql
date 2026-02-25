---- 1️⃣ Total spend per customer using CTE
With Customer_Spend AS(
    select customer_id, sum(amount) AS Total_Spend
    from orders
    Group By customer_id)
select * from Customer_Spend where Total_spend >800;

----2️⃣ Join CTE with customers

WITH customer_spend AS (
    SELECT customer_id,
           SUM(amount) AS total_spend
    FROM orders
    GROUP BY customer_id
)

SELECT c.name,
       cs.total_spend
FROM customers c
JOIN customer_spend cs
ON c.customer_id = cs.customer_id;





