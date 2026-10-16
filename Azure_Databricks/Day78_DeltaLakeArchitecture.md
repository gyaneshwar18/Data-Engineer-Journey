Day 78 — Delta Lake Architecture

90-Day Data Engineering Journey | Azure Databricks + ADLS Gen2

Today's topic is Delta Lake Architecture. We'll learn how Delta Lake stores data, how its transaction log works, and why Data Engineers use Delta Lake instead of relying only on CSV files.

As agreed, this lesson includes the concept, hands-on notebooks, expected outputs, and interview questions at the end—all in one response.

We'll continue with your existing Sales.csv dataset and your configured ADLS Gen2 storage.

1. Concept — What, Why, and Where?
1.1 What is Delta Lake?

Delta Lake is a storage layer that adds reliability and transaction capabilities to data lakes.

It uses Parquet data files and a transaction log to manage the data.

With a regular CSV file, we can store and read data, but CSV alone doesn't provide Delta Lake's transaction management, schema enforcement, or time-travel capabilities.

Delta Lake adds these capabilities to data lake storage.

Why do Data Engineers use Delta Lake?

Delta Lake provides:

ACID transactions: Helps ensure reliable, consistent data operations.
Schema enforcement: Helps prevent writes that don't conform to the expected schema.
Time travel: Allows access to previous table versions when the required historical data is still available.
Updates and deletes: Supports data modifications beyond simple file replacement.
Transaction logging: Tracks committed changes to the table.

We'll study these features individually in the upcoming days of our roadmap.

1.2 CSV vs. Parquet vs. Delta Lake
Feature	CSV	Parquet	Delta Lake
Data format	Text	Columnar	Parquet data files plus transaction log
Supports tabular data	Yes	Yes	Yes
Transaction log	No	No, by itself	Yes
ACID transactions	No, by itself	No, by itself	Yes
Schema enforcement	Not built in	Limited format-level support	Yes
Time travel	No built-in support	No built-in support	Yes

Important: Delta Lake is not simply another file format like CSV. It manages a table using data files and a transaction log.

1.3 Delta Lake Architecture

This is the main concept for Day 78.

             Azure Databricks
                    |
                    v
             PySpark DataFrame
                    |
                    v
              Delta Lake
                    |
           +--------+---------+
           |                  |
           v                  v
     Parquet Files       Transaction Log
     Actual Data         _delta_log/
           |                  |
           |                  |
           v                  v
      Sales Records     Tracks Table Changes
                         and File Versions

Let's understand the two main components.

Component 1: Parquet Data Files

These files store the actual table data.

For example, your sales records include:

Item_Identifier
Item_Type
Item_MRP
Item_Outlet_Sales

When we write the DataFrame in Delta format, the data is stored in Parquet files rather than ordinary CSV output files.

Component 2: Transaction Log

Delta Lake creates a directory named:

_delta_log/

This log records table changes and transaction information.

For example, after the first successful Delta write, the directory commonly contains a log file similar to:

_delta_log/
    00000000000000000000.json

The log allows Delta Lake to determine which data files belong to a committed table version.

As the table changes, additional transaction log entries are created. Delta Lake can also create checkpoint files to make log processing more efficient.

Remember:

Parquet files store the data.
_delta_log records the table's transactions and state.

This distinction is essential for understanding Delta Lake.

2. Hands-on Setup — Your Existing Environment

We'll use the existing configuration you established earlier.

Setting	Value
Storage account	datalakegyan
Source container	source
Input file	Sales.csv
Destination container	destination
Output path	sales.csv
Authentication	Your configured managed identity and Unity Catalog external locations
Source path
source_path = "abfss://source@datalakegyan.dfs.core.windows.net/Sales.csv"
Destination path
destination_path = "abfss://destination@datalakegyan.dfs.core.windows.net/sales.csv"
Important before writing

In Day 76, we wrote CSV output to the destination path.

Today, we'll use that same destination path for Delta format to stay aligned with your existing setup.

This changes the contents of the destination from CSV output to Delta data. The path remains named sales.csv, but after this exercise it will be a Delta table directory, not a regular CSV file. We will not delete or modify your source file.

If you need to preserve the previous CSV output, do not run the cleanup or write steps below until you've decided where the Delta output should go.

3. Step-by-Step Coding

We'll organize the practical work into two notebooks.

Notebook 1: 01_delta_lake_architecture
Task 1 — Read Sales.csv

What are we doing?

Reading the source CSV into a Spark DataFrame. This is the starting point for converting the data into Delta format.

Code:

source_path = "abfss://source@datalakegyan.dfs.core.windows.net/Sales.csv"

sales_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(source_path)

display(sales_df)

Expected output: Your existing sales records appear in Databricks.

The DataFrame is now available for writing in Delta format.

Task 2 — Inspect the schema

Why?

We should understand the structure of our source data before writing it into the Delta table.

Code:

sales_df.printSchema()

Expected output: Spark displays the column names and data types, such as Item_Identifier, Item_Type, Item_MRP, and Item_Outlet_Sales.

The actual data types depend on the source data and schema inference.

Task 3 — Prepare the destination

Before writing Delta data, we need to ensure the output path is not still occupied by the previous CSV output.

Run this inspection first:

destination_path = "abfss://destination@datalakegyan.dfs.core.windows.net/sales.csv"

display(
    dbutils.fs.ls(
        "abfss://destination@datalakegyan.dfs.core.windows.net/"
    )
)

If sales.csv/ exists from Day 76, inspect its contents:

display(
    dbutils.fs.ls(destination_path)
)

If the path contains only the CSV output created during Day 76, and you are ready to replace that output with Delta data, run:

dbutils.fs.rm(destination_path, True)

Warning: This removes the entire sales.csv output path and its contents. Run it only after confirming that the path contains the previous output you intend to replace. Do not run it if the path contains data you need to preserve.

If the destination doesn't exist, you can skip the deletion step.

Task 4 — Write the DataFrame in Delta format

What are we doing?

Writing the sales DataFrame in Delta format rather than CSV.

Code:

sales_df.write \
    .format("delta") \
    .mode("overwrite") \
    .save(destination_path)

Explanation:

Code	Purpose
.format("delta")	Selects Delta Lake as the storage format.
.mode("overwrite")	Replaces existing output at the specified path.
.save(destination_path)	Writes the Delta data to ADLS Gen2.

Expected result: The cell should complete successfully without an exception.

After a successful write, the destination contains Parquet data files and a _delta_log directory.

This is the key practical task for Day 78.

Notebook 2: 02_verify_delta_architecture

Now we'll verify that the output is actually stored in Delta format.

Task 5 — Read the Delta data

Code:

destination_path = "abfss://destination@datalakegyan.dfs.core.windows.net/sales.csv"

delta_df = spark.read \
    .format("delta") \
    .load(destination_path)

display(delta_df)

Expected output: Your sales records appear again.

Notice that we used:

.format("delta")

We must use the matching format when reading the Delta data.

This is different from reading a regular CSV file with .csv().

Task 6 — Inspect the Delta directory

What are we doing?

Checking whether Delta Lake created its data files and transaction log.

Code:

display(
    dbutils.fs.ls(destination_path)
)

Expected structure:

sales.csv/
    _delta_log/
    part-....snappy.parquet
    part-....snappy.parquet

The number of data files can vary.

You should see the _delta_log directory and one or more Parquet files after a successful write.

Task 7 — Inspect the transaction log

Code:

display(
    dbutils.fs.ls(
        destination_path + "/_delta_log/"
    )
)

Expected output: A listing of the Delta transaction log files.

After the initial write, you would typically see a JSON transaction log file representing the initial table version.

For example:

00000000000000000000.json

Additional files may appear depending on the operations performed and the Delta Lake configuration.

Task 8 — Verify the table's schema and sample records

Code:

delta_df.printSchema()

display(delta_df.limit(10))

Expected result:

Spark displays the table schema.
Up to ten sales records appear.
The data should correspond to the sales dataset written from the source.

We use limit(10) here to inspect a small sample rather than performing another full row count on a potentially large dataset.

4. Verification Checklist

Once you've executed both notebooks, verify the following:

Check	Expected result
Read the source CSV	Successful
Inspect the schema	Column names and data types displayed
Write using Delta format	Successful
Read using Delta format	Data displayed
Inspect destination	Delta data files visible
Inspect _delta_log	Transaction log files visible

If you receive an error, share the exact error message. We'll troubleshoot the relevant step before continuing.

5. Interview Preparation
A. Common Interview Questions
Q1. What is Delta Lake?

Answer: Delta Lake is a storage layer that adds capabilities such as ACID transactions, schema enforcement, and time travel to data lakes. It manages table data using Parquet files and a transaction log.

Q2. What is the architecture of Delta Lake?

Answer: Delta Lake stores the actual table data in Parquet files and maintains a _delta_log directory containing transaction information. The log allows Delta Lake to identify the committed table state.

Q3. What is the purpose of _delta_log?

Answer: It tracks table transactions and changes, including information about data files added or removed and the table's state at different versions.

Q4. Where is the actual data stored in a Delta table?

Answer: The actual records are stored in Parquet data files. The transaction log manages which files belong to the table at a particular version.

Q5. What are ACID transactions?

Answer: ACID stands for:

Atomicity: An operation is committed as a transaction rather than being partially committed.
Consistency: A successful transaction preserves the table's defined consistency rules.
Isolation: Concurrent operations are managed to avoid exposing inconsistent intermediate states.
Durability: Once a transaction is committed, its result is recorded durably.

Delta Lake uses transaction-log-based mechanisms to provide ACID transactions for supported table operations.

Q6. What is the difference between CSV and Delta Lake?

Answer: CSV is a text-based data format. Delta Lake manages data files, typically in Parquet format, alongside a transaction log that provides capabilities such as ACID transactions, schema enforcement, and time travel.

Q7. How do you write a DataFrame in Delta format?

Answer:

df.write \
    .format("delta") \
    .mode("overwrite") \
    .save(path)
Q8. How do you read a Delta table stored at a path?

Answer:

df = spark.read \
    .format("delta") \
    .load(path)
Q9. Does Delta Lake store all historical copies of the data forever?

Answer: No. Historical access depends on retained data files and transaction-log information. Retention settings and cleanup operations can make older versions unavailable.

Q10. Is Delta Lake the same as Parquet?

Answer: No. Parquet is a columnar data file format. Delta Lake uses Parquet data files together with a transaction log to provide additional table-management capabilities.

B. Twisted and Scenario-Based Questions
Q11. If a Delta table contains Parquet files, why can't you simply read the directory as Parquet and expect complete Delta behavior?

Answer: Reading the directory as Parquet reads the files as ordinary Parquet data and bypasses Delta's transaction log. It may include files that don't represent the current committed table state.

Use the Delta reader when you need Delta table semantics:

spark.read.format("delta").load(path)
Q12. You see Parquet files in storage. Does that prove the directory is a Delta table?

Answer: No. Parquet files can exist without Delta Lake. To verify a path is managed as Delta, check for a valid transaction log and read it with the Delta reader.

Q13. What happens if the transaction log is missing?

Answer: Delta Lake cannot reliably reconstruct the table's committed state without the required log information. The table may become unreadable as a Delta table, even if some Parquet files remain.

Q14. A write operation fails. Could partially written files still exist?

Answer: Yes. Physical data files may exist even when a transaction hasn't successfully committed. Delta Lake uses its transaction log to distinguish committed table state from uncommitted or unreferenced files.

Q15. If you overwrite a Delta table, what happens to its previous versions?

Answer: Overwriting creates a new committed table version. Previous versions may remain accessible through time travel while the required historical data and log information are retained. They aren't necessarily deleted immediately.

Q16. If the Delta log tracks changes, does it store a complete copy of every table for every version?

Answer: No. The log records transaction actions and table-state changes. Delta Lake uses these records and the associated data files to reconstruct a version, rather than necessarily storing a complete table copy for each version.

Q17. What is the difference between a Delta table and a Delta table's storage path?

Answer: A storage path is the location where the table's files are stored. A Delta table is the logical table represented by the data files and transaction log at that location, or by a catalog table definition that refers to the storage location.

Q18. How would you explain today's hands-on exercise in an interview?

Answer:

"I read a sales CSV file from Azure Data Lake Storage Gen2 into a PySpark DataFrame in Azure Databricks. I wrote the DataFrame in Delta format, read it back using the Delta reader, and inspected the storage directory and transaction log to understand how Delta Lake stores and manages table data."

6. Day 78 — Repository Notes

After completing and verifying the practical tasks, add these notes to your Data-Engineer-Journey repository.

Day 78: Delta Lake Architecture

Objective: Understand Delta Lake architecture and write a PySpark DataFrame in Delta format.

Concepts learned:

Delta Lake and its purpose.
CSV versus Parquet versus Delta Lake.
Parquet data files.
The _delta_log directory.
ACID transactions.
Schema enforcement.
Time travel and historical data retention.
Reading and writing Delta data using PySpark.

Practical pipeline:

ADLS Gen2
    |
    | Sales.csv
    v
Azure Databricks / PySpark
    |
    | Read CSV
    v
Spark DataFrame
    |
    | Write in Delta format
    v
ADLS Gen2
    |
    +---- Parquet Data Files
    |
    +---- _delta_log/

Completion checklist:

 Understand Delta Lake architecture.
 Read the sales CSV.
 Write the DataFrame in Delta format.
 Read the Delta data back.
 Inspect the Parquet data files.
 Inspect the transaction log.
 Review interview and twisted questions.
 Save concise notes in the repository.