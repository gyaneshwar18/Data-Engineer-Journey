# Star Schema

Fact Table:
- Stores metrics
- Example: Revenue, Sales, Quantity

Dimension Tables:
- Store descriptive attributes
- Customer
- Product
- Date
- Store

Benefits:
- Faster analytics
- Simpler queries
- BI friendly

Example:

           dim_customer
                 |
                 |
dim_product -- fact_sales -- dim_date
                 |
                 |
            dim_store

