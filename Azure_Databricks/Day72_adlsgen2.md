Day 72 — Azure Data Lake Storage Gen2 (ADLS Gen2)
1. What is ADLS Gen2?
Azure Data Lake Storage Gen2 is cloud storage used to store raw files and processed data for data engineering pipelines.
Why do we use it?
- Store CSV, JSON, Parquet and other data.
- Provide storage for Azure Databricks and PySpark.
- Organize data into raw, processed and curated layers.
Your setup:
- Storage account: datalakegyan
- Container: source
- Authentication: Access Connector + Managed Identity
- Unity Catalog credential: datalake-managed-identity
- External location: source-location
2. Understand the architecture
Source files — CSV / JSON / API
ADLS Gen2 — datalakegyan/source

Azure Databricks + PySpark
Transformed data

3. Verify your storage account
In Azure Portal:
1. Open Storage accounts → datalakegyan.
2. Open Configuration.
3. Confirm Hierarchical namespace = Enabled.
4. Open Containers → source.
5. Confirm the container exists.
No need to create another storage account or container.
4. Verify access from Databricks
Run in a Python notebook cell:
storage_path = "abfss://source@datalakegyan.dfs.core.windows.net/"display(dbutils.fs.ls(storage_path))



Expected: a list of files and folders, or an empty listing if the container has no files.
5. Create the raw and processed folders
base_path = "abfss://source@datalakegyan.dfs.core.windows.net/"dbutils.fs.mkdirs(base_path + "raw/")dbutils.fs.mkdirs(base_path + "processed/")



Verify:
display(dbutils.fs.ls(base_path))



6. Create sample employee data
data = [    (1, "Ravi", 30000),    (2, "Priya", 45000),    (3, "Kiran", 40000)]columns = ["id", "name", "salary"]df = spark.createDataFrame(data, columns)display(df)



Expected: three employee rows.
7. Write data to ADLS Gen2
raw_path = "abfss://source@datalakegyan.dfs.core.windows.net/raw/employees/"df.write \    .mode("overwrite") \    .option("header", True) \    .csv(raw_path)



8. Read the data back
employees_df = spark.read \    .option("header", True) \    .option("inferSchema", True) \    .csv(raw_path)display(employees_df)



9. Transform the data
Select employees whose salary is at least 40,000.
from pyspark.sql.functions import colhigh_salary_df = employees_df.filter(    col("salary") >= 40000)display(high_salary_df)



Expected: Priya and Kiran.
10. Write the transformed data
processed_path = "abfss://source@datalakegyan.dfs.core.windows.net/processed/high_salary_employees/"high_salary_df.write \    .mode("overwrite") \    .option("header", True) \    .csv(processed_path)



Verify:
display(dbutils.fs.ls(processed_path))



Spark writes CSV output as a directory containing part files, not necessarily as one single CSV file.
11. Understand authentication
Your configured access path is:
Azure Databricks
      ↓
Unity Catalog external location
      ↓
Storage credential: datalake-managed-identity
      ↓
Access Connector: ac-databricks-learning
      ↓
ADLS Gen2: datalakegyan/source


The external location's read/write checks passed earlier. File Events permissions were not verified; they are optional for the basic read/write exercises above.
12. Common errors
Error	Check
403 AuthorizationFailure	Storage role assignment and Unity Catalog privileges
Path does not exist	Container and path spelling
Permission denied	External location permissions and managed identity
No files displayed	Confirm files exist in the container
CSV schema looks incorrect	Check header=True and inferSchema=True
13. Interview questions
Q1. What is ADLS Gen2?
Azure cloud storage designed for analytics workloads, with hierarchical namespace support.
Q2. What is a container?
A logical grouping of files and directories inside a storage account.
Q3. What is the difference between ADLS and Databricks?
ADLS stores data; Databricks processes and transforms data.
Q4. How does Databricks access ADLS in your setup?
Through Unity Catalog's external location and storage credential using an Azure managed identity.
Q5. What is the raw layer?
The layer where incoming source data is stored before significant transformations.