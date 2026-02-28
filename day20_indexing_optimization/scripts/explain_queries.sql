SELECT * FROM orders
WHERE customer_id = 5000;


EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE customer_id = 5000;

CREATE INDEX idx_customer_id
ON orders(customer_id);

EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE customer_id = 5000;