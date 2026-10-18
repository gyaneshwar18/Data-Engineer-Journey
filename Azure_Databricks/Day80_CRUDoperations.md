Day 80 — Delta Lake CRUD Operations + Transaction Log

90-Day Data Engineering Journey | Azure Databricks + PySpark

Today's lesson covers how to insert, read, update, and delete records in a Delta table, and how to inspect the transaction history of those operations.

We'll use your existing Sales dataset and the managed Delta table created on Day 79. This lets us practise without modifying your existing external Delta data at destination/sales.csv.

1. Concept — What, Why, and Where?
1.1 What are CRUD operations?

CRUD stands for four basic operations used to manage data.

Operation	Meaning	SQL command
C — Create	Add a record	INSERT
R — Read	Retrieve records	SELECT
U — Update	Modify existing records	UPDATE
D — Delete	Remove records from the current table	DELETE

Imagine a company maintains a sales table. The business needs to add a sales record, retrieve it, correct its sales amount, and eventually remove it.

Delta Lake supports these operations on Delta tables.

1.2 Why do we need CRUD operations?

In real-world Data Engineering, data isn't always loaded once and left unchanged.

For example:

A new sales record arrives.
An existing record needs correction.
An incorrect record needs removal.
A Data Engineer needs to verify what changed and when.

Delta Lake provides reliable table modifications along with transaction history.

1.3 What is the Delta transaction log?

A Delta table contains two important components:

Delta Table
    |
    +---- Parquet Files
    |       Stores actual data
    |
    +---- _delta_log/
            Records committed table changes

When a Delta table is modified, Delta Lake records the committed operation in its transaction log.

For example:

Version 0 → Initial table creation
Version 1 → Insert record
Version 2 → Update record
Version 3 → Delete record

These version numbers are illustrative. The actual versions depend on the table's existing history and operations.

Each committed modification creates a new table version. You can inspect the operations using DESCRIBE HISTORY.

Important: Deleting a record from the latest table version does not necessarily erase its old physical data immediately. Historical files may remain until they are removed by an appropriate cleanup operation, which we'll cover on Day 82.

2. Hands-on Coding — Complete Day 80

We'll use two notebooks.

Notebook	Purpose
01_delta_crud_operations	Practise INSERT, SELECT, UPDATE and DELETE
02_delta_transaction_log	Inspect table history and metadata



Now run this in a SQL notebook cell:

```sql
CREATE TABLE sales
USING DELTA
LOCATION 'abfss://destination@datalakegyan.dfs.core.windows.net/sales_delta';
```

This registers the existing Delta data with the table name `sales`. It does not copy the data again.

Note: This requires the appropriate Unity Catalog permissions and an eligible external location. The table is an external table because you specify its storage location.

## Step 3: Retrieve data using SQL

Now you can query the table directly:

```sql
SELECT *
FROM sales
LIMIT 5;
```

Filter rows:

```sql
SELECT Item_Type, Item_MRP
FROM sales
WHERE Item_MRP > 100;
```

Calculate total sales by item type:

```sql
SELECT Item_Type,
       SUM(Item_Outlet_Sales) AS total_sales
FROM sales
GROUP BY Item_Type;
```

## Step 4: Modify data using SQL

Delta tables support data modifications.

Update:

```sql
UPDATE sales
SET Item_MRP = Item_MRP + 10
WHERE Item_Type = 'Dairy';
```

Delete:

```sql
DELETE FROM sales
WHERE Item_MRP < 10;
```

These statements modify the Delta table, not your original `source/Sales.csv` file. Make sure the columns and values match your actual data before running them.

## Step 5: Verify your changes

```sql
SELECT *
FROM sales
WHERE Item_Type = 'Dairy'
LIMIT 10;
```

## Common Interview Questions

### Q1. What does CRUD stand for?

**Answer:** CRUD stands for Create, Read, Update and Delete. In SQL, these operations commonly correspond to `INSERT`, `SELECT`, `UPDATE` and `DELETE`.

### Q2. How do you insert a record into a Delta table?

**Answer:**

```
INSERTINTO catalog_name.schema_name.table_name
    (Item_Identifier, Item_Type)VALUES
    ('ITEM001','Dairy');
```

The column list and values must match the table's schema.

### Q3. How do you update a record in a Delta table?

**Answer:**

```
UPDATE catalog_name.schema_name.table_nameSET Item_Outlet_Sales=250.0WHERE Item_Identifier='ITEM001';
```

The `WHERE` clause identifies the records to update.

### Q4. How do you delete selected records from a Delta table?

**Answer:**

```
DELETEFROM catalog_name.schema_name.table_nameWHERE Item_Identifier='ITEM001';
```

Without a `WHERE` clause, a `DELETE` statement can delete all rows in the table, so the condition must be checked carefully.

### Q5. What is the Delta transaction log?

**Answer:** The Delta transaction log records committed table changes and helps Delta Lake determine the table's state at a particular version.

### Q6. How do you check Delta table history?

**Answer:**

```
DESCRIBE HISTORY catalog_name.schema_name.table_name;
```

This displays operation history, timestamps and version information.

### Q7. Does every successful update create a new Delta table version?

**Answer:** Each committed table modification creates a new version. If an operation fails before committing, it does not create a successfully committed version for that operation.

### Q8. Does DELETE immediately remove the old physical data?

**Answer:** Not necessarily. A deleted record is removed from the latest logical table state, but historical data files can remain until cleanup removes them.

### Q9. What is the difference between the transaction log and the Parquet files?

**Answer:**

- Parquet files store the table's data.
- The transaction log records changes and identifies which data files belong to a committed table version.

### Q10. Why do Data Engineers inspect table history?

**Answer:** They can review past operations, identify when changes occurred, and investigate unexpected modifications to a table.

## B. Twisted and Scenario-Based Questions

### Q11. You deleted a record, but the storage directory still contains old Parquet files. Did DELETE fail?

**Answer:** Not necessarily. Delta Lake can remove a record from the current logical table without immediately deleting all historical physical files. The transaction log determines the current table state. Physical cleanup is a separate operation.

### Q12. You executed UPDATE, but the record still shows the old value. What would you check?

**Answer:** I would verify the update condition, confirm that it matched the intended record, inspect the table after the operation, and check for errors. I would also ensure that I'm querying the same table that was updated.

### Q13. Why should you avoid running UPDATE or DELETE without a WHERE clause during a practice exercise?

**Answer:** Without a condition, the operation may affect every record. A narrowly scoped condition helps protect existing business data.

### Q14. If a record is deleted, can you always recover it using the transaction log?

**Answer:** Not always. Recovery depends on the availability of the required historical log information and data files. Retention and cleanup operations can make older versions unavailable. Table history should not be treated as a permanent backup.

### Q15. Does the Delta transaction log store a complete copy of the entire table after every operation?

**Answer:** No. It records transaction actions and table-state changes. Delta Lake uses the log and data files to determine the table's state at a given version.

### Q16. What happens if you insert the same business record twice?

**Answer:** Unless the pipeline or table design prevents duplicates, both rows may be inserted. Delta Lake does not automatically deduplicate records simply because their values are identical. Data Engineers must implement appropriate uniqueness or deduplication logic.

### Q17. What is the difference between UPDATE and MERGE?

**Answer:**

- `UPDATE` modifies existing matching rows.
- `MERGE` supports matching source and target data to apply different actions, such as updating existing records and inserting new records.