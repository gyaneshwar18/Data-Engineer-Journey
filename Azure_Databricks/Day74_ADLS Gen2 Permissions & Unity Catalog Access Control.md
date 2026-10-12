Your Existing Setup
Component	Name
Storage account	datalakegyan
Container	source
Access Connector	ac-databricks-learning
Storage credential	datalake-managed-identity
External location	source-location
2. Understand the Permission Flow
Azure Databricks
       ↓
Unity Catalog Permissions
       ↓
External Location: source-location
       ↓
Storage Credential
       ↓
Managed Identity
       ↓
ADLS Gen2

There are two permission layers:

Azure IAM: Controls what the managed identity can do in storage.
Unity Catalog: Controls what Databricks users can do through the external location.
3. Verify External Location Access

In your Databricks notebook, run:

storage_path = "abfss://source@datalakegyan.dfs.core.windows.net/"

display(dbutils.fs.ls(storage_path))

If successful, your notebook can list the container's contents.

4. Test Write Permission
test_path = "abfss://source@datalakegyan.dfs.core.windows.net/day74_test/"

dbutils.fs.mkdirs(test_path)

display(dbutils.fs.ls(storage_path))
5. Test Read and Write Using PySpark

Create sample data:

data = [
    (1, "Ravi"),
    (2, "Priya"),
    (3, "Kiran")
]

df = spark.createDataFrame(data, ["id", "name"])

Write it:

output_path = "abfss://source@datalakegyan.dfs.core.windows.net/day74_test/employees/"

df.write.mode("overwrite").parquet(output_path)

Read it:

employees_df = spark.read.parquet(output_path)

display(employees_df)
6. Understand Unity Catalog Permissions

Open Catalog → External Locations → source-location → Permissions.

Review which users, groups, or service principals have privileges on the external location.

Common privileges include:

Privilege	Purpose
READ FILES	Read files through the external location
WRITE FILES	Write files through the external location
CREATE EXTERNAL TABLE	Create external tables using the location

You need appropriate Unity Catalog privileges and underlying Azure storage permissions. Do not change permissions unnecessarily if your existing setup works.

7. Interview Questions

Q1. What is the difference between Azure IAM and Unity Catalog permissions?

Azure IAM grants cloud resource access; Unity Catalog governs data access within Databricks.

Q2. What does READ FILES allow?

It allows reading files through an external location, subject to the applicable storage permissions.

Q3. What does WRITE FILES allow?

It allows writing files through an external location, subject to the applicable storage permissions.

Q4. Why use a managed identity?

It avoids storing and rotating client secrets for the Azure identity used to access storage.