1. Concept — What, Why, and Where?
1.1 What is Auto Loader?

Auto Loader is a Databricks feature that incrementally discovers and processes files arriving in cloud storage. It supports ADLS Gen2 and file formats such as CSV, JSON and Parquet.

Without Auto Loader

Suppose a company receives sales files every day. A basic batch pipeline might need to be run repeatedly to discover and load the new files.

With Auto Loader

Auto Loader keeps track of discovered files and processes new arrivals incrementally.

Azure Data Lake Storage Gen2
             |
             | Sales.csv
             v
     Databricks Auto Loader
             |
             | Detect and read files
             v
       Spark DataFrame
             |
             v
       Further Processing
1.2 Important Auto Loader concepts
Concept	Meaning
cloudFiles	The Structured Streaming source used by Auto Loader
cloudFiles.format	Specifies the input format, such as CSV
cloudFiles.schemaLocation	Stores inferred schema information
checkpointLocation	Tracks streaming progress and discovered files
readStream	Creates a streaming DataFrame

Auto Loader uses its schema location to track schema information and its checkpoint to track ingestion progress.

Today's goal: Read your existing Sales.csv using Auto Loader and verify that the data is processed successfully.

2. Practical Notebook

Create one notebook named:

Day83_Auto_Loader

We'll execute the following cells in order.

Cell 1 — Verify the Source File

Code:

source_folder = (
    "abfss://source@datalakegyan.dfs.core.windows.net/"
)

display(dbutils.fs.ls(source_folder))

Expected output: The file Sales.csv should appear in the listing.

This checks that Databricks can access your existing source container.

Cell 2 — Configure Auto Loader

We'll use your existing destination container for Auto Loader's metadata.

The schema and checkpoint directories are operational metadata, not additional sales datasets.

metadata_path = (
    "abfss://destination@datalakegyan.dfs.core.windows.net/"
    "_day83_autoloader"
)

schema_path = metadata_path + "/schema"

checkpoint_path = metadata_path + "/checkpoint"

Understand the paths:

schema_path: Stores the inferred schema.
checkpoint_path: Stores the stream's progress and state.

These locations must be writable by your configured identity.

Cell 3 — Read Sales.csv Using Auto Loader

Code:

sales_stream_df = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("cloudFiles.schemaLocation", schema_path)
    .option("cloudFiles.inferColumnTypes", "true")
    .option("cloudFiles.includeExistingFiles", "true")
    .option("header", "true")
    .load(source_folder)
)

sales_stream_df.printSchema()
Understand the code
Code	Purpose
spark.readStream	Creates a streaming read
.format("cloudFiles")	Uses Auto Loader
cloudFiles.format = csv	Reads CSV files
cloudFiles.schemaLocation	Saves schema information
cloudFiles.inferColumnTypes = true	Asks Auto Loader to infer column data types
cloudFiles.includeExistingFiles = true	Includes existing files when initializing the stream
.load(source_folder)	Reads files from the source directory

Auto Loader normally infers CSV columns as strings. Setting cloudFiles.inferColumnTypes to true asks it to infer more specific data types.

Expected output

You should see columns similar to:

root
 |-- Item_Identifier: string
 |-- Item_Weight: double
 |-- Item_Fat_Content: string
 |-- Item_Visibility: double
 |-- Item_Type: string
 |-- Item_MRP: double
 |-- Outlet_Identifier: string
 |-- Outlet_Establishment_Year: integer
 |-- Outlet_Size: string
 |-- Outlet_Location_Type: string
 |-- Outlet_Type: string
 |-- Item_Outlet_Sales: double

The actual inferred data types may differ.

Cell 4 — Process the File and Verify the Output

For this introductory exercise, we'll use Spark's console sink to inspect the records without writing another copy of the sales data.

Code:

query = (
    sales_stream_df.writeStream
    .format("console")
    .outputMode("append")
    .option("checkpointLocation", checkpoint_path)
    .option("truncate", "false")
    .option("numRows", "5")
    .trigger(availableNow=True)
    .start()
)

query.awaitTermination()

print("Auto Loader processing completed.")
Expected output

The notebook's streaming logs should show a batch containing records from Sales.csv, followed by:

Auto Loader processing completed.

The console sink displays the data for verification; it does not create a destination sales table.

Important: On the first run, Auto Loader should process the existing Sales.csv. If you rerun the notebook with the same checkpoint, it normally won't process that same unchanged file again. This is expected behavior.

If your Databricks environment reports an error, share the exact message so we can troubleshoot it.

3. Day 83 — Interview Questions
Common Questions

Q1. What is Auto Loader?

Auto Loader is a Databricks feature that incrementally discovers and processes new files arriving in cloud storage.

Q2. What is cloudFiles?

cloudFiles is the Structured Streaming source used to read data through Auto Loader.

Q3. Why do we use Auto Loader instead of spark.read.csv()?

spark.read.csv() reads a CSV as a batch. Auto Loader supports incremental file discovery and tracks ingestion progress, making it suitable for files that arrive over time.

Q4. What is cloudFiles.schemaLocation?

It specifies where Auto Loader stores inferred schema information and tracks schema changes.

Q5. What is checkpointLocation?

It specifies where Spark stores checkpoint information, including streaming progress, so the stream can resume without unnecessarily reprocessing previously handled files.

Q6. Can Auto Loader read files from ADLS Gen2?

Yes. It supports ADLS Gen2 paths using the abfss:// scheme.

Twisted and Scenario-Based Questions

Q7. You rerun Auto Loader, but it doesn't process Sales.csv again. Is that an error?

Not necessarily. If the stream uses the same checkpoint and the file was already processed, Auto Loader normally skips that unchanged file.

Q8. What happens if the checkpoint is deleted?

The stream loses its saved progress information. Restarting without the checkpoint can cause previously processed files to be processed again, depending on the new stream configuration.

Q9. What happens when a new column appears in an incoming CSV file?

Auto Loader supports schema evolution. Depending on the configured schema evolution mode, it can update the schema and may stop the stream so it can restart with the updated schema.

Q10. Does Auto Loader automatically store the data in Delta Lake?

No. Auto Loader reads the incoming data. The pipeline must separately define where and how the data is written, such as to a Delta table.

Q11. What is the difference between Auto Loader and Structured Streaming?

Structured Streaming is Spark's streaming processing engine. Auto Loader is a Databricks source built on Structured Streaming that specializes in incrementally discovering files in cloud storage.

Q12. What did you implement today?

"I configured Auto Loader in Azure Databricks to read my existing sales CSV from ADLS Gen2. I configured schema tracking and checkpointing, processed the file through a streaming query, and inspected the resulting records."