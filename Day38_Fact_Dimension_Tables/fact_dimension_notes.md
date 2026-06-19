# Fact Tables vs Dimension Tables

Fact Table:
- Stores metrics
- Revenue
- Sales
- Quantity
- Profit

Dimension Table:
- Stores descriptive data
- Customer
- Product
- Date
- Store

Primary Key:
- Exists in Dimension Tables

Foreign Key:
- Stored in Fact Tables

Example:

fact_sales
-----------
sale_id
customer_id
product_id
date_id
amount

dim_customer
------------
customer_id
customer_name
city

dim_product
-----------
product_id
product_name
category
