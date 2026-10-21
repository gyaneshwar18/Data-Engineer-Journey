Day 82 — VACUUM + OPTIMIZE + ZORDER

90-Day Data Engineering Journey | Azure Databricks + Delta Lake

We'll continue using your existing external Delta table, sales, created on Day 80.

Table location:

abfss://destination@datalakegyan.dfs.core.windows.net/sales_delta

Today's lesson uses simple SQL notebooks. We'll cover the concepts and practical coding first, followed by interview questions and twisted scenarios at the end.

1. Concept — What, Why, and Where?
1.1 OPTIMIZE — Improve File Layout

When data is written into a Delta table, Spark may create many small files.

Having too many small files can increase the overhead of reading data.

OPTIMIZE combines small data files into fewer, more appropriately sized files. This is called file compaction.

Example:

Before OPTIMIZE:

sales/
├── part-001.parquet
├── part-002.parquet
├── part-003.parquet
├── part-004.parquet
└── part-005.parquet

After OPTIMIZE:

sales/
├── part-A.parquet
└── part-B.parquet

Illustration only. The actual number of files depends on the data and execution.

1.2 ZORDER — Improve Data Skipping

ZORDER organizes related data values together across files so that Delta Lake can skip files that don't contain values needed by a query.

For example, your table has an Item_MRP column, and you might frequently execute:

SELECT Item_Type, Item_MRP
FROM sales
WHERE Item_MRP > 100;

ZORDER can improve data skipping for suitable queries that filter on the chosen column.

Important: ZORDER is not guaranteed to improve every query. Databricks recommends liquid clustering for new table designs, but we'll learn ZORDER because it is part of our existing roadmap.

1.3 VACUUM — Remove Unused Data Files

When a Delta table is updated or deleted, some previous data files may no longer belong to its current version.

Those files can remain in storage because Delta Lake uses transaction history to manage table versions.

VACUUM removes eligible, unused data files from the table's storage location. The default retention threshold is seven days.

Example:

Delta table storage
       |
       +-- Current data files
       |       Retained
       |
       +-- Old, unused files
               |
               v
          VACUUM
               |
               v
       Eligible files removed

Critical warning: VACUUM can remove files required to query older table versions. Because we practised Time Travel on Day 81, we'll first use DRY RUN to inspect the files that would be deleted. Do not execute the actual cleanup until you've reviewed its impact.

2. Hands-on Coding — SQL Notebooks

We'll create two simple notebooks.

Notebook	Purpose
01_OPTIMIZE_ZORDER	Compact files and organize data
02_VACUUM	Preview unused files and understand cleanup
Notebook 1: 01_OPTIMIZE_ZORDER
Task 1 — Check the current data

Run this SQL cell:

SELECT Item_Identifier, Item_Type, Item_MRP, Item_Outlet_Sales
FROM sales
LIMIT 10;

Expected result: Up to ten rows from your existing Delta table.

This gives us a simple reference before optimization.

Task 2 — Run OPTIMIZE
OPTIMIZE sales;

What happens?

Delta Lake optimizes the file layout, typically by compacting smaller files.

Expected result: Databricks reports information about files added and removed during optimization.

Your table's logical data should remain unchanged.

Task 3 — Run ZORDER

We'll use Item_MRP as our example because we previously used it in filtering queries.

OPTIMIZE sales
ZORDER BY (Item_MRP);

What happens?

Delta Lake reorganizes the data layout using Item_MRP as the Z-order column. This can help skip irrelevant files in queries that filter on this column.

ZORDER works as part of OPTIMIZE, so this operation also optimizes the file layout.

Task 4 — Verify the data

Run:

SELECT Item_Identifier, Item_Type, Item_MRP, Item_Outlet_Sales
FROM sales
LIMIT 10;

The query should return the table's data as before. OPTIMIZE and ZORDER change the physical file layout, not the intended logical contents of the table.

Notebook 2: 02_VACUUM
Task 1 — Preview eligible files

Run:

VACUUM sales DRY RUN;

What happens?

Databricks lists eligible files that the VACUUM operation would delete, up to 1,000 files.

Important: DRY RUN previews the deletion candidates without deleting them.

You might see files listed, or no files if there are no eligible files to remove.

Task 2 — Review the table history

Before considering an actual VACUUM operation, inspect the history:

DESCRIBE HISTORY sales;

Review the recorded versions and operations.

Remember that removing historical data files may make older versions unavailable for Time Travel.

Task 3 — Actual VACUUM (Optional)

Do not run this step yet if you still need to practise Time Travel on older versions.

After reviewing the dry-run results and confirming that the historical data you need is no longer required, the standard command is:

VACUUM sales;

This removes eligible files according to the configured retention threshold. The default is seven days. Databricks recommends retaining at least seven days and warns against reducing the retention interval without understanding the risks.

For our learning exercise, running VACUUM sales DRY RUN is sufficient to practise safely. We'll leave the actual cleanup optional because it can permanently remove files required for historical queries.

3. Day 82 — Interview Questions
A. Common Questions

Q1. What is OPTIMIZE in Delta Lake?

OPTIMIZE improves Delta table file layout, typically by compacting smaller files into fewer files.

Q2. What is ZORDER?

ZORDER organizes related values together across files to help Delta Lake skip files that aren't relevant to a query.

Q3. What is VACUUM?

VACUUM removes unused data files that are eligible for deletion based on the configured retention threshold.

Q4. What is the default VACUUM retention threshold?

The default threshold is seven days.

Q5. Does OPTIMIZE change the logical contents of the table?

No. Its purpose is to improve the physical data layout. Queries should return the same logical data before and after OPTIMIZE.

Q6. Does ZORDER run independently of OPTIMIZE?

No. In Delta Lake, ZORDER is specified through an OPTIMIZE command.

Q7. What does VACUUM ... DRY RUN do?

It previews the files eligible for deletion without deleting them.

B. Twisted and Scenario-Based Questions

Q8. You ran OPTIMIZE, but a query is still slow. Why?

The query might be slow for reasons unrelated to small files, such as an inefficient query plan, a large scan, insufficient compute, or a filter that doesn't benefit from the chosen layout.

Q9. Does ZORDER always improve performance?

No. Its benefit depends on the query patterns, selected columns, data distribution, and table size.

Q10. Can VACUUM break Time Travel?

It can make older versions unavailable if the data files needed by those versions are removed.

Q11. You ran VACUUM sales DRY RUN. Were any files deleted?

No. A dry run only previews eligible files.

Q12. Why shouldn't you run VACUUM with zero-hour retention casually?

A very short retention period can delete files needed by running operations or historical queries. Databricks provides a safety check and recommends retaining at least seven days.

Q13. What is the difference between OPTIMIZE and VACUUM?

OPTIMIZE: Improves the physical layout of data files.
VACUUM: Removes eligible, unused data files.

Q14. Why might a Data Engineer run OPTIMIZE before VACUUM?

OPTIMIZE improves the file layout, while VACUUM cleans up eligible files that are no longer needed. They solve different problems and can be scheduled according to workload and retention requirements.

Q15. What did you practise today?

"I optimized my existing Delta table, used ZORDER to demonstrate data layout optimization, and ran VACUUM in dry-run mode to inspect eligible files without deleting them."