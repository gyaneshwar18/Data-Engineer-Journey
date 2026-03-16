CREATE TABLE IF NOT EXISTS fact_orders_incremental (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    status VARCHAR(20),
    amount NUMERIC
);