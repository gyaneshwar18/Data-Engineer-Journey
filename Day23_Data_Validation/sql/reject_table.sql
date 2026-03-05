CREATE TABLE IF NOT EXISTS rejected_orders (
    customer_id INT,
    order_date TEXT,
    amount TEXT,
    status TEXT,
    reason TEXT
);