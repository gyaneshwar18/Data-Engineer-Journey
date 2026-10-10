Day 71 — DBFS + File Handling
1. What is DBFS?
DBFS (Databricks File System) is a filesystem interface historically used to access files in Databricks.
Why do we use it?
To access, list, and manage files used in data processing.
Where is it used?
For accessing input files, checking file locations, and managing data files.
Important: DBFS root and mounts are legacy approaches. Modern Databricks development generally prefers Unity Catalog volumes and cloud storage locations such as Azure Data Lake Storage (ADLS).
2. Basic Commands
List files
dbutils.fs.ls("dbfs:/")


Lists files and directories at the specified DBFS path, if that path is available in your environment.
Create a directory
dbutils.fs.mkdirs("dbfs:/tmp/day71")


Creates the directory if the path is supported.
Copy a file
dbutils.fs.cp(    "dbfs:/tmp/source.csv",    "dbfs:/tmp/copy.csv")


The source file must exist, and both paths must be accessible.
Remove a file
dbutils.fs.rm("dbfs:/tmp/copy.csv")


Warning: This deletes the file. Use it only for test files you no longer need.
3. Read a CSV Using PySpark
Once you have a CSV file at an accessible path:
df = spark.read.csv(    "dbfs:/path/to/customers.csv",    header=True,    inferSchema=True)df.show()


Replace the example path with your actual file path.
What happens?
CSV File
   ↓
Spark reads the file
   ↓
DataFrame
   ↓
Transformations

4. How Is This Used in Azure Databricks?
In a real Azure Data Engineering project, files are commonly stored in ADLS Gen2.
Azure Data Lake Storage
          ↓
Azure Databricks
          ↓
PySpark
          ↓
DataFrame
          ↓
Transformations

Example ADLS path:
adls_path = "abfss://container@storageaccount.dfs.core.windows.net/raw/customers.csv"


Read the file:
df = spark.read.csv(    adls_path,    header=True,    inferSchema=True)df.show()


This requires appropriate storage permissions and authentication.
Remember: DBFS and ADLS are not the same thing. ADLS is Azure cloud storage; DBFS is a Databricks filesystem interface.
5. Most Asked Interview Questions
Q1. What is DBFS?
DBFS is a Databricks filesystem interface historically used to access and manage files.
Q2. What is the difference between DBFS and ADLS?
ADLS is Azure's cloud storage service. DBFS is a Databricks filesystem interface.
Q3. How do you list files using Databricks utilities?
dbutils.fs.ls("dbfs:/")


Q4. How do you read a CSV file using PySpark?
df = spark.read.csv(    file_path,    header=True,    inferSchema=True)


Q5. Should we use DBFS root for new production projects?
Generally, no. Prefer supported storage approaches such as Unity Catalog volumes and direct cloud storage access.