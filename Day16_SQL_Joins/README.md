# SQL JOINs (Inner Join, Left Join, Aggregation After Join)

## 📌 Objective
Learn how to combine data from multiple tables using SQL JOIN operations.  
JOINs are one of the most important SQL skills for data engineering because most real datasets are relational and require table enrichment.

This module focuses on inner joins, left joins, null handling, and aggregations after joins.

---

## 🧠 Concepts Covered

- INNER JOIN
- LEFT JOIN
- JOIN conditions using keys
- Primary key ↔ foreign key joins
- Handling unmatched rows with NULL
- Finding missing relationships
- Aggregation after join
- Multi-table query pattern
- Table aliasing


## 🗄️ Tables Used

Two related tables:

### customers
- customer_id (primary key)
- name
- city

### orders
- order_id
- customer_id (foreign key)
- amount

Relationship:
customers.customer_id = orders.customer_id

---

## 🧱 Schema Setup (schema_setup.sql)

```sql
CREATE TABLE customers (
    customer_id INT,
    name TEXT,
    city TEXT
);

INSERT INTO customers VALUES
(1,'Riya','Hyderabad'),
(2,'Aryan','Mumbai'),
(3,'Sneha','Delhi'),
(4,'Rahul','Pune');


CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    amount INT
);

INSERT INTO orders VALUES
(101,1,500),
(102,1,700),
(103,2,300),
(104,5,900);
