# Description

This project focuses on understanding database indexing and query optimization.
Indexing is used in databases to improve the speed of data retrieval operations.

When a query searches for data in a table without an index, the database must scan every row in the table. This is called a full table scan and can be very slow when the table contains millions of records.

An index works like the index of a book. Instead of reading every page to find information, the database uses the index to directly locate the required rows.

In this exercise, indexes are created on columns that are frequently used in queries. After creating indexes, query performance can be analyzed using execution plans.


# Indexes are commonly used on:

primary keys

foreign keys

columns used in WHERE clauses

columns used in JOIN operations


# Understanding indexing helps when:

designing databases

optimizing analytics queries

building high-performance pipelines
