TRUNCATE TABLE daily_sales_summary;

INSERT INTO daily_sales_summary(order_date, total_sales, order_count)
SELECT
order_date,
SUM(amount),
COUNT(*)
FROM orders
GROUP BY order_date;