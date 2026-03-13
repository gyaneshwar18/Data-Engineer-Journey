INSERT INTO daily_sales_summary(order_date, total_sales, order_count)
SELECT
order_date,
SUM(amount) AS total_sales,
COUNT(*) AS order_count
FROM orders
GROUP BY order_date;