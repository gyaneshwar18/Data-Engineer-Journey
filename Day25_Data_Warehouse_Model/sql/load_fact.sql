INSERT INTO fact_orders(customer_id, order_date, status, amount)
SELECT
customer_id,
order_date,
status,
amount
FROM orders;