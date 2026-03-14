INSERT INTO dim_customer(customer_id)
SELECT DISTINCT customer_id
FROM orders;

INSERT INTO dim_date(order_date, year, month, day)
SELECT DISTINCT
order_date,
EXTRACT(YEAR FROM order_date),
EXTRACT(MONTH FROM order_date),
EXTRACT(DAY FROM order_date)
FROM orders;

INSERT INTO dim_status(status)
SELECT DISTINCT status
FROM orders;