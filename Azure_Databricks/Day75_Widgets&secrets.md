Day 75 — Databricks dbutils, Widgets & Secrets

Goal: Learn how to manage files, accept notebook inputs, and securely handle secrets in Azure Databricks.

Your existing ADLS Gen2 connection will be reused.

1. dbutils — File Operations

dbutils provides utilities for working with files and other Databricks features.

List files
storage_path = "abfss://source@datalakegyan.dfs.core.windows.net/"

display(dbutils.fs.ls(storage_path))
Create a directory
dbutils.fs.mkdirs(
    "abfss://source@datalakegyan.dfs.core.windows.net/day75/"
)
Copy a file
dbutils.fs.cp(
    "abfss://source@datalakegyan.dfs.core.windows.net/input.csv",
    "abfss://source@datalakegyan.dfs.core.windows.net/day75/input_copy.csv"
)

Run this only if input.csv exists.

2. Widgets — Accept Notebook Inputs

Widgets allow users to pass parameters to a notebook without changing its code.

Create a text widget
dbutils.widgets.text("department", "IT", "Department")
Read the value
department = dbutils.widgets.get("department")

print("Selected department:", department)
Use the widget value
data = [
    (1, "Ravi", "IT"),
    (2, "Priya", "HR"),
    (3, "Kiran", "IT")
]

df = spark.createDataFrame(
    data,
    ["id", "name", "department"]
)

filtered_df = df.filter(
    df.department == department
)

display(filtered_df)

Change the widget value to HR and rerun the cells.

Dropdown widget
dbutils.widgets.dropdown(
    "environment",
    "dev",
    ["dev", "test", "prod"],
    "Environment"
)

environment = dbutils.widgets.get("environment")

print(environment)
3. Secrets — Securely Store Credentials

Purpose: Avoid hardcoding passwords, API keys, and client secrets in notebooks.

In Azure Databricks, secrets are commonly managed using secret scopes.

Read a secret
secret_value = dbutils.secrets.get(
    scope="my-secret-scope",
    key="my-secret-key"
)

Replace the scope and key with your actual configured names.

Note: This code works only if the secret scope and secret already exist and you have permission to access them. Do not print the secret value.

You do not need to create a secret for your existing ADLS connection because it uses a managed identity.

4. Real-World Data Engineering Example

Suppose a pipeline processes data for a selected department.

dbutils.widgets.text("department", "IT", "Department")

department = dbutils.widgets.get("department")

input_path = (
    "abfss://source@datalakegyan.dfs.core.windows.net/"
    "raw/employees/"
)

df = spark.read.option(
    "header", True
).option(
    "inferSchema", True
).csv(input_path)

result_df = df.filter(
    df.department == department
)

display(result_df)

The department can be changed without modifying the transformation logic.

5. Interview Questions

Q1. What is dbutils?

A collection of Databricks utilities for file operations, widgets, secrets, and other tasks.

Q2. What are widgets?

Widgets allow users to pass parameters into notebooks at runtime.

Q3. Why use secrets?

To protect sensitive credentials instead of hardcoding them in notebooks.

Q4. What is the difference between widgets and secrets?

Widgets accept configurable inputs; secrets securely retrieve sensitive values.

Q5. Do we need a client secret for our current ADLS setup?

No. Your existing Access Connector and managed identity provide storage authentication.

6. Day 75 Checklist
 List files using dbutils.fs.ls().
 Create a directory using dbutils.fs.mkdirs().
 Create and read a text widget.
 Create and read a dropdown widget.
 Understand secret scopes and secret retrieval.
 Understand why managed identity avoids client secrets for your ADLS connection.

