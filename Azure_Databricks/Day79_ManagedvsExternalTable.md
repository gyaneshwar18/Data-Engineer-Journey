Day 79 — Managed vs. External Delta Tables

90-Day Data Engineering Journey | Azure Databricks + ADLS Gen2

Today's practical work uses your existing Sales.csv dataset and your configured Unity Catalog environment.

We'll organize the lesson into three notebooks, followed by interview questions and twisted scenarios.

1. Concept — Managed vs. External Tables
1.1 What is a table in Databricks?

A table lets you query structured data using SQL or PySpark.

For example, instead of reading a CSV file every time, you can register the data as a table and query it:

SELECT * FROM some_table;

Databricks supports managed and external tables.

1.2 Managed Table

A managed table is a table whose storage location and data lifecycle are managed by Unity Catalog.

You specify the table name, and Databricks manages where the underlying data is stored.

Sales.csv
    |
    v
Azure Databricks
    |
    v
Managed Delta Table
    |
    v
Storage managed by Unity Catalog

Key point: You manage the table through Databricks without having to specify its physical storage path.

1.3 External Table

An external table is a table for which you specify an existing storage location.

Unity Catalog manages the table's metadata and access governance, while you manage the underlying files and their lifecycle.

ADLS Gen2
    |
    | destination/sales.csv
    v
Delta Data + _delta_log
    |
    v
External Delta Table
    |
    v
Query using SQL or PySpark

In our case, we'll register an external table over the existing Delta data at destination/sales.csv.

Important: Creating the external table registers the existing data. It does not require copying the data to another path.

1.4 Main Differences
Feature	Managed Table	External Table
Storage location	Determined by Unity Catalog	Specified by you
Data lifecycle	Managed by Unity Catalog	Managed by you
Table metadata	Managed by Unity Catalog	Managed by Unity Catalog
Specify LOCATION	Normally not required	Required
Storage path	Managed storage location	Existing external storage path
Drop table	Data files are scheduled for deletion according to the platform's retention behavior	Table metadata is removed; underlying data files remain
Best suited for	Tables you want Databricks to manage	Existing data whose storage lifecycle you control

Databricks generally recommends managed tables for new tables, while external tables are useful when you need to retain control of an existing storage location.

Remember this for interviews

Managed table = Databricks manages the storage location and data lifecycle.

External table = You specify the storage location and manage the underlying data lifecycle.

Both table types are governed by Unity Catalog.

2. Hands-on Setup

We'll use your existing configuration.

Setting	Value
Storage account	datalakegyan
Source	source/Sales.csv
Delta destination	destination/sales.csv
Managed identity	datalake-managed-identity
Source external location	source-location
Destination external location	destination-location

Prerequisite: This lesson assumes Day 78 successfully created a Delta table at destination/sales.csv.

We will not modify the source CSV or overwrite the existing destination Delta data during today's external-table registration.

Notebook 1: 01_create_managed_table
Task 1 — Read the source data
source_path = "abfss://source@datalakegyan.dfs.core.windows.net/Sales.csv"

sales_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(source_path)

display(sales_df.limit(10))

Expected output: The first ten sales records appear in Databricks.

Task 2 — Find your current catalog and schema

A Unity Catalog table must belong to a catalog and schema.

Run:

context = spark.sql("""
    SELECT
        current_catalog() AS catalog_name,
        current_schema() AS schema_name
""")

display(context)

Expected output: Databricks displays your current catalog and schema.

We'll use these values instead of assuming a particular catalog or schema name.

Task 3 — Create a managed Delta table

What are we doing?

Creating a managed Delta table from the same sales dataset.

Because this is a managed table, we won't specify an ADLS storage path. Unity Catalog determines its managed storage location.

Run:

catalog_name = context.first()["catalog_name"]
schema_name = context.first()["schema_name"]

managed_table = (
    f"{catalog_name}.{schema_name}.day79_sales_managed"
)

sales_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(managed_table)

print("Managed table created:", managed_table)

Expected output:

Managed table created: <your_catalog>.<your_schema>.day79_sales_managed

The actual catalog and schema names depend on your Databricks environment.

Important: This creates a managed table containing a copy of the same source data in Unity Catalog-managed storage. It doesn't modify Sales.csv or overwrite destination/sales.csv.

The overwrite mode replaces the contents of this specifically named managed table if it already exists. Use this code only for the tutorial table.

Task 4 — Read the managed table
managed_df = spark.table(managed_table)

display(managed_df.limit(10))

Expected output: The sales records appear from your managed Delta table.

Now let's work with the external table.

Notebook 2: 02_create_external_table
Task 5 — Verify the existing Delta location

Set the existing output path:

destination_path = (
    "abfss://destination@datalakegyan.dfs.core.windows.net/sales.csv"
)

Check its contents:

display(
    dbutils.fs.ls(destination_path)
)

Check the transaction log:

display(
    dbutils.fs.ls(destination_path + "/_delta_log/")
)

Expected output: The destination should contain Delta data files and a _delta_log directory.

If _delta_log is missing, stop here. The destination has not been verified as a Delta table, and we should resolve that before registering an external Delta table.

Task 6 — Register an external Delta table

What are we doing?

Registering the existing Delta data at the destination path in Unity Catalog.

We are not writing or copying the sales records again.

Run:

external_table = (
    f"{catalog_name}.{schema_name}.day79_sales_external"
)

spark.sql(f"""
    CREATE TABLE IF NOT EXISTS {external_table}
    USING DELTA
    LOCATION '{destination_path}'
""")

print("External table registered:", external_table)

Expected output:

External table registered: <your_catalog>.<your_schema>.day79_sales_external

The table name will use your actual catalog and schema.

Why do we specify LOCATION here?

Because an external table references data at a storage location that you specify.

The path is the existing Delta destination covered by your configured external location.

If Unity Catalog reports a permission or external-location error, share the exact error rather than changing your existing identity configuration.

Task 7 — Read the external table
external_df = spark.table(external_table)

display(external_df.limit(10))

Expected output: The existing sales records appear from the external table.

The external table references destination/sales.csv; it doesn't create another copy of the data.

Notebook 3: 03_compare_delta_tables
Task 8 — Inspect the managed table
display(
    spark.sql(f"DESCRIBE EXTENDED {managed_table}")
)

This displays the table metadata, including information about its type and storage.

Task 9 — Inspect the external table
display(
    spark.sql(f"DESCRIBE EXTENDED {external_table}")
)

Compare the metadata for both tables.

The managed table uses Unity Catalog-managed storage. The external table uses your explicitly specified ADLS Gen2 location.

Task 10 — Query both tables

Managed table:

display(
    spark.sql(f"""
        SELECT Item_Type, Item_Outlet_Sales
        FROM {managed_table}
        LIMIT 10
    """)
)

External table:

display(
    spark.sql(f"""
        SELECT Item_Type, Item_Outlet_Sales
        FROM {external_table}
        LIMIT 10
    """)
)

Expected output: Both queries display sales data.

The purpose is to demonstrate that SQL can query both managed and external tables. The managed table stores a copy of the dataset, whereas the external table references your existing Delta data.

3. Practical Verification Checklist
Verification	Expected result
Read source CSV	Successful
Identify catalog and schema	Names displayed
Create managed table	Successful
Query managed table	Sales records displayed
Verify external Delta path	_delta_log exists
Register external table	Successful
Query external table	Sales records displayed
Inspect table metadata	Managed and external types distinguishable

Important: We are not dropping either table today. Dropping a managed table and dropping an external table have different effects on the underlying data.

4. Interview Questions — Managed vs. External Delta Tables
A. Frequently Asked Questions
Q1. What is a managed table in Databricks?

A managed table is a table whose storage location and data lifecycle are managed by Unity Catalog.

Q2. What is an external table?

An external table is a table for which you specify a storage location. Unity Catalog manages its metadata and access governance, while the underlying files remain under your storage lifecycle control.

Q3. What is the biggest difference between a managed and external table?

The main difference is who manages the underlying data storage and its lifecycle.

Managed: Unity Catalog manages it.
External: You manage it.
Q4. Do both tables support Delta Lake?

Yes. Both managed and external tables can use Delta format.

Q5. Why do we specify LOCATION when creating an external table?

Because the table references data at a storage path that we specify.

Q6. What happens when you drop a managed table?

Unity Catalog removes the table and schedules the underlying data files for deletion according to its managed-table retention behavior.

Q7. What happens when you drop an external table?

Unity Catalog removes the table metadata, but the underlying files remain at the external storage location.

Q8. Which table type is generally recommended for new tables in Databricks?

Managed tables are generally recommended because Databricks can manage the data lifecycle and provide managed-table optimizations. External tables are useful when you need to control the underlying storage location and lifecycle.

Q9. Can an external table point to an existing Delta table path?

Yes. You can register an existing Delta location as an external table, provided that the location and permissions meet Unity Catalog's requirements.

Q10. Are the data files stored inside Unity Catalog itself?

No. The data remains in cloud storage in your account. For a managed table, Unity Catalog controls the storage location and lifecycle; for an external table, you specify and manage the underlying location.

B. Twisted and Scenario-Based Questions
Q11. You drop an external table. Is the data deleted from ADLS Gen2?

Answer: No. Dropping the external table removes the catalog metadata but leaves the underlying data files in storage.

Q12. You drop a managed table. Does the data remain available at the table's old location indefinitely?

Answer: No. Unity Catalog manages the lifecycle of the underlying data files, including deletion according to the platform's retention behavior.

Q13. Can two external tables point to the same Delta location?

Technically, multiple table registrations can reference the same location, but this can create metadata and consistency-management risks. Databricks advises against registering the same external table across multiple metastores. Avoid multiple registrations unless you have a deliberate and well-managed design.

Q14. If both tables use Delta format, why do we need two types?

Delta format determines how the data and transactions are stored. Managed versus external determines how the table's underlying storage location and lifecycle are managed.

Q15. The business needs the data to remain in a specific ADLS Gen2 location. Which table type would you consider?

Answer: An external table, because I can specify the storage location and retain control over the underlying files' lifecycle.

Q16. A team wants Databricks to manage the storage lifecycle instead of handling paths manually. Which table type would you generally recommend?

Answer: A managed table, assuming the team's requirements fit Unity Catalog's managed-storage model.

Q17. An external table is registered in Unity Catalog. Does that mean nobody can access its files outside Databricks?

Answer: No. An external table's files remain in cloud storage, and users with direct cloud-storage permissions may be able to access them outside Databricks. Unity Catalog's table governance doesn't automatically prevent all direct external access.

Q18. What did you implement in today's practical exercise?

Answer:

"I read the existing sales CSV into a PySpark DataFrame and created a managed Delta table from that data. I then registered the existing Delta location in ADLS Gen2 as an external table using Unity Catalog. Finally, I queried both tables and inspected their metadata to understand the difference between managed and external storage."

5. Day 79 — Repository Notes

Add these notes to your Data-Engineer-Journey repository after verifying the practical work.

Topic: Managed vs. External Delta Tables

Concepts learned:

Managed Delta tables.
External Delta tables.
Unity Catalog's role in table governance.
Managed storage versus user-specified storage locations.
Creating a managed table with saveAsTable().
Registering an existing Delta path using CREATE TABLE ... LOCATION.
Different table-drop behaviors.

Completion checklist:

 Understand managed versus external tables.
 Create and query the managed table.
 Verify the existing Delta destination.
 Register and query the external table.
 Inspect the metadata of both tables.
 Review interview and twisted questions.