DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    amount INT
);

INSERT INTO orders VALUES
(101,1,500),
(102,1,700),
(103,2,300),
(104,2,400),
(105,3,900),
(106,3,600),
(107,4,200);