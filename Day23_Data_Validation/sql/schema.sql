CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    amount NUMERIC(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL
);