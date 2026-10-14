1. Concept — What, Why, and Where?
What is Data Ingestion?

Data ingestion means bringing data from a source into a system where we can process and analyze it.

For our practical exercise:

Source: Sales.csv in ADLS Gen2.
Processing engine: Azure Databricks with PySpark.
Destination: sales.csv in the ADLS Gen2 destination container.
Our pipeline
ADLS Gen2
    |
    | Sales.csv
    v
Azure Databricks
    |
    | PySpark reads CSV
    v
Spark DataFrame
    |
    | Write CSV
    v
ADLS Gen2
    |
    | sales.csv
    v
Destination
Why do we need this?

Imagine a company receives millions of sales records in CSV files.

A Data Engineer needs to:

Read the source data.
Understand its structure.
Process the data using Spark.
Store the result for downstream processing.

Interview point: Data ingestion is the process of collecting and loading data from source systems into a target system for processing, storage, or analysis.

2. Hands-on Setup — Your Actual Environment

We'll use your existing configuration.

Setting	Your configuration
Storage account	datalakegyan
Source container	source
Input file	Sales.csv
Destination container	destination
Output location	sales.csv
Compute	Your existing Databricks compute
Authentication	Configured managed identity and Unity Catalog external locations
Input path
source_path = "abfss://source@datalakegyan.dfs.core.windows.net/Sales.csv"
Output path
destination_path = "abfss://destination@datalakegyan.dfs.core.windows.net/sales.csv"

Important: source and destination are separate containers, not folders within the same container.

We'll use the managed identity and external locations you already configured. No additional authentication setup is required for this lesson.

3. Step-by-Step Coding

Open your existing Azure Databricks notebook.

We'll run each task separately. Run Task 1 first and share the output before proceeding.

Task 1 — Read the CSV File
What are we doing?

Reading Sales.csv from ADLS Gen2 into a Spark DataFrame.

Code
source_path = "abfss://source@datalakegyan.dfs.core.windows.net/Sales.csv"

sales_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(source_path)

display(sales_df)
Understand the code
Code	Purpose
spark.read	Starts reading data using Spark.
.option("header", True)	Uses the first CSV row as column names.
.option("inferSchema", True)	Asks Spark to infer column data types.
.csv(source_path)	Reads the CSV at the specified path.
display(sales_df)	Displays the DataFrame in Databricks.
Expected output

You should see sales records with columns similar to these:

Item_Identifier
Item_Weight
Item_Fat_Content
Item_Visibility
Item_Type
Item_MRP
Outlet_Identifier
Outlet_Establishment_Year
Outlet_Size
Outlet_Location_Type
Outlet_Type
Item_Outlet_Sales

The displayed rows should contain your actual source data.

Your task: Run Task 1 and tell me whether the data appears correctly or whether you receive an error.

We'll verify it before moving to Task 2.

4. Verification — How We'll Validate the Pipeline

We'll verify the following throughout today's lesson:

 Spark successfully reads the source CSV.
 Column names and data types are correct.
 We can inspect the number of records.
 Spark writes the data to the destination.
 We can read the destination data back successfully.

If anything fails, share the error message. We'll troubleshoot it before continuing.

One important detail: Spark's CSV writer normally creates a directory containing part files, rather than a single physical CSV file. We'll verify the actual destination structure when we reach that task.

5. Interview Preparation

We'll cover the questions now so you can connect the concepts to today's practical work.

Q1. What is data ingestion?

Answer: Data ingestion is the process of collecting data from source systems and loading it into a target system for further processing or analysis.

Q2. How do you read a CSV file using PySpark?

Answer:

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("path/to/file.csv")

header=True uses the first row as column names. inferSchema=True asks Spark to infer data types.

Q3. What is a Spark DataFrame?

Answer: A Spark DataFrame is a distributed collection of data organized into named columns. Spark can process it across multiple partitions.

Q4. What is the difference between header=True and inferSchema=True?

Answer:

header=True: Determines column names from the first row.
inferSchema=True: Attempts to determine column data types from the data.

These options solve different problems.

Q5. Why use Spark instead of pandas for a very large CSV?

Answer: Spark can distribute processing across multiple workers, making it suitable for large datasets. Pandas typically processes a DataFrame in the memory of a single machine.

Twisted Question 6. Does spark.read.csv() immediately load the entire CSV into memory?

Answer: Not in the same way as a typical eager, in-memory DataFrame load. Spark generally uses lazy evaluation: reading a file defines a DataFrame, and Spark executes the necessary work when an action requires results.

Twisted Question 7. Is inferSchema=True always the best choice for production pipelines?

Answer: No. Schema inference can require additional data scanning and may produce unexpected types. In production pipelines, an explicitly defined schema is often preferable for predictable processing.

Twisted Question 8. If display(sales_df) works, does that prove the entire dataset has been processed?

Answer: No. display() may retrieve only the rows needed for the displayed output. It does not necessarily process every row in the dataset.