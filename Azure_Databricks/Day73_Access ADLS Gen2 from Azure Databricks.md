Access ADLS Gen2 from Azure Databricks

Access ADLS Gen2 from Azure Databricks
1. Objective

Practice reading, writing, listing, and managing files in your existing ADLS Gen2 container using your configured Unity Catalog external location.

2. Your Existing Setup
Component	Value
Storage account	datalakegyan
Container	source
Storage credential	datalake-managed-identity
External location	source-location
Authentication	Access Connector + Managed Identity

No new credentials or connections are required.

3. List Files
storage_path = "abfss://source@datalakegyan.dfs.core.windows.net/"

display(dbutils.fs.ls(storage_path))
4. Create a Test Folder
test_path = "abfss://source@datalakegyan.dfs.core.windows.net/day73_test/"

dbutils.fs.mkdirs(test_path)

Verify:

display(dbutils.fs.ls(storage_path))
5. Create a Sample DataFrame
data = [
    (1, "Ravi", 30000),
    (2, "Priya", 45000),
    (3, "Kiran", 40000)
]

columns = ["id", "name", "salary"]

df = spark.createDataFrame(data, columns)

display(df)
6. Write Data to ADLS
output_path = "abfss://source@datalakegyan.dfs.core.windows.net/day73_test/employees/"

df.write \
    .format("csv") \
    .mode("overwrite") \
    .option("header", True) \
    .save(output_path)
7. Read Data Back
employees_df = spark.read \
    .format("csv") \
    .option("header", True) \
    .option("inferSchema", True) \
    .load(output_path)

display(employees_df)
8. Filter Data
from pyspark.sql.functions import col

high_salary_df = employees_df.filter(
    col("salary") >= 40000
)

display(high_salary_df)
9. Save Processed Data
processed_path = "abfss://source@datalakegyan.dfs.core.windows.net/day73_test/high_salary/"

high_salary_df.write \
    .format("csv") \
    .mode("overwrite") \
    .option("header", True) \
    .save(processed_path)
10. Verify the Output
display(dbutils.fs.ls(
    "abfss://source@datalakegyan.dfs.core.windows.net/day73_test/"
))
11. Interview Questions

Q1. How does Databricks access your ADLS Gen2 storage?

Through Unity Catalog's external location and storage credential, backed by an Azure managed identity.

Q2. What does abfss:// mean?

It is the secure filesystem URI scheme used to access Azure Data Lake Storage through the Hadoop ABFS driver.

Q3. Why use mode("overwrite")?

To replace existing output data at the specified path.

Q4. Does creating a DataFrame automatically save it to ADLS?

No. We must explicitly write it using operations such as df.write.csv() or df.write.format(...).save().