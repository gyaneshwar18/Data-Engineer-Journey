CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id INT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS dim_date (
    order_date DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT
);

CREATE TABLE IF NOT EXISTS dim_status (
    status VARCHAR(20) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS fact_orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    status VARCHAR(20),
    amount NUMERIC,
    FOREIGN KEY(customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY(order_date) REFERENCES dim_date(order_date),
    FOREIGN KEY(status) REFERENCES dim_status(status)
);