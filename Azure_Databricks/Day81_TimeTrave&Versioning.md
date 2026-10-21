Day 81 — Data Versioning + Time Travel

90-Day Data Engineering Journey | Azure Databricks + Delta Lake

Today's lesson uses your existing Delta table, sales, from Day 80. We'll use simple SQL notebooks to view table history and query previous versions of the data.

1. Concept — Data Versioning and Time Travel
What is Data Versioning?

Whenever a Delta table is modified through a committed operation, Delta Lake creates a new table version.

For example:

Version 0 → Initial data
Version 1 → INSERT
Version 2 → UPDATE
Version 3 → DELETE

These version numbers are illustrative.

Each version represents the table's state after a committed operation.

What is Time Travel?

Time Travel allows us to query an earlier version of a Delta table.

Example: Suppose you accidentally updated the sales prices. You can query a previous version to see what the data looked like before that update.

Delta Lake supports querying older versions using a version number or timestamp.

Where does the history come from?

Delta Lake maintains the transaction log in the _delta_log directory.

Delta Table
    |
    +-- Parquet Files → Data
    |
    +-- _delta_log/   → Transactions and versions

Remember:

DESCRIBE HISTORY shows table operations.
VERSION AS OF queries a particular version.
TIMESTAMP AS OF queries the version associated with a particular time.
2. Hands-on Coding — SQL Notebook

Create one notebook named:

Day81_Data_Versioning_Time_Travel

We'll use your existing Day 80 table:

Table: sales

Location:
abfss://destination@datalakegyan.dfs.core.windows.net/sales_delta

Important: Today's exercises only read historical versions. They do not update, delete, or overwrite your data.

Task 1 — View Table History

Run this SQL cell:

DESCRIBE HISTORY sales;
Expected output

You'll see information similar to:

version	timestamp	operation
3	Example timestamp	DELETE
2	Example timestamp	UPDATE
1	Example timestamp	WRITE

The output depends on your actual table history. Newer versions appear first.

Your task: Find the version and timestamp of an operation you performed on Day 80.

For example, locate the UPDATE operation.

Task 2 — Read the Current Data

Run:

SELECT *
FROM sales
LIMIT 5;

This returns up to five records from the current version of the table.

On Day 80, you updated Dairy prices and deleted rows whose Item_MRP was below 10.

The current data reflects those changes if the operations completed successfully.

Task 3 — Query an Earlier Version

Look at the history from Task 1.

Choose a version from before the update or delete operation you want to inspect.

Replace <version_number> below with that actual version number.

SELECT *
FROM sales VERSION AS OF <version_number>
LIMIT 5;

For example, if the version you selected was 2, the query would be:

SELECT *
FROM sales VERSION AS OF 2
LIMIT 5;

Do not assume version 2 exists in your table. Use a version number from your actual history.

What should happen?

Databricks returns data from the selected historical version instead of the current table version.

If you select a version before the Day 80 update, the Dairy prices should reflect the earlier state.

Time Travel requires the historical data and log information to remain available.

Task 4 — Query a Version Using a Timestamp

Instead of specifying a version number, you can specify a timestamp.

First, find the timestamp in the output of:

DESCRIBE HISTORY sales;

Copy the timestamp for the historical version you want to query.

Then run:

SELECT *
FROM sales TIMESTAMP AS OF '<timestamp_from_history>'
LIMIT 5;

Important: Replace <timestamp_from_history> with the actual timestamp from your table history, keeping it inside single quotes.

This retrieves the table snapshot corresponding to that timestamp.

Task 5 — Compare Current and Historical Data

Suppose you want to check Dairy prices before and after the Day 80 update.

Current data
SELECT
    Item_Identifier,
    Item_Type,
    Item_MRP
FROM sales
WHERE Item_Type = 'Dairy'
LIMIT 10;
Historical data

Replace <version_number> with the version from before the update.

SELECT
    Item_Identifier,
    Item_Type,
    Item_MRP
FROM sales VERSION AS OF <version_number>
WHERE Item_Type = 'Dairy'
LIMIT 10;

Compare the results.

If the historical version is from before the update and contains the same Dairy records, you should be able to observe the difference in Item_MRP.

This is a practical example of investigating a previous data state without modifying the current table.

3. Day 81 — Interview Questions
Common Questions

Q1. What is Delta Lake Time Travel?

Time Travel allows us to query earlier versions of a Delta table using a version number or timestamp.

Q2. How do you check Delta table history?

DESCRIBE HISTORY sales;

It returns information about operations and table versions.

Q3. How do you query an earlier version?

SELECT *
FROM sales VERSION AS OF 2;

The version number must exist and its required historical data must still be available.

Q4. Can we use a timestamp instead of a version number?

Yes.

SELECT *
FROM sales TIMESTAMP AS OF '2026-10-18T12:00:00.000+00:00';

Use an appropriate timestamp from your actual table history rather than assuming this example timestamp exists.

Q5. Does Time Travel modify the current table?

No. A Time Travel query reads a historical snapshot. It does not roll back or change the current table.

Twisted and Scenario-Based Questions

Q6. You accidentally updated records. How can you inspect the previous data?

Answer: I would run DESCRIBE HISTORY, identify a version before the incorrect update, and query it using VERSION AS OF.

Q7. Does Delta Lake keep every version forever?

Answer: No. Historical data and transaction logs have retention policies. Once necessary historical data files are removed, older versions may no longer be queryable.

Q8. What is the difference between Time Travel and rollback?

Answer: Time Travel queries an earlier version without changing the current table. A rollback changes the current table state to an earlier state.

Q9. You can see an old version in the history, but the Time Travel query fails. Why?

Answer: The data files required for that version may no longer be available, even if some history information remains. I would inspect the error and the table's retention and cleanup history.

Q10. Is Time Travel a replacement for a backup?

Answer: No. Time Travel is useful for investigating historical data states, but it depends on retained historical files and transaction logs. It should not be treated as a permanent backup.