Day 70 — Databricks Compute & Spark Cluster
1. What is Compute?
Compute provides the resources required to run your Databricks code.
Notebook
   ↓
Compute
   ↓
Spark
   ↓
Data Processing

Why do we need it?
Your notebook contains the code, but compute executes that code.
2. What is a Spark Cluster?
A Spark cluster is the processing environment where Spark distributes the work.
Basic structure:
Spark Cluster
     │
 ┌───┴────┐
Driver   Executors
           │
        Tasks

Driver
Coordinates the Spark application.
Executors
Actually process the data and execute tasks.
3. Basic Flow
When you run:
df.show()


Conceptually:
Notebook
   ↓
Driver
   ↓
Creates execution plan
   ↓
Executors
   ↓
Process data
   ↓
Result

4. Hands-on
In your Databricks notebook, check the Spark version:
print(spark.version)


Create a DataFrame:
data = [    (1, "Rahul"),    (2, "Priya"),    (3, "Amit")]df = spark.createDataFrame(    data,    ["id", "name"])df.show()


Check the execution plan:
df.explain()


You don't need to deeply study the plan yet. We already covered explain() during PySpark performance.
5. How this is used in Azure Databricks
In Azure Databricks:
Azure Databricks Workspace
          ↓
       Compute
          ↓
   Spark Cluster
      ↓       ↓
   Driver  Executors
             ↓
       Data Processing

You create/select Databricks compute and attach your notebook to it. Your PySpark/SQL code then runs using that compute.
6. Important Interview Questions
Q1. What is Databricks Compute?
Compute provides the processing resources required to run notebooks and Spark workloads in Databricks.

Q2. What is a Spark cluster?
A Spark cluster is a group of processing resources where Spark distributes and executes data processing tasks.

Q3. What is the role of the Driver?
The Driver coordinates the Spark application, creates the execution plan, and distributes tasks to executors.

Q4. What is an Executor?
An Executor is a process that runs Spark tasks and performs the actual data processing.

Q5. Driver vs Executor?
Driver coordinates the work; Executors perform the work.

Q6. Where does our PySpark code run?
In Databricks, PySpark code runs through Spark on the Databricks compute resources.

7. Remember This
Compute
   ↓
Spark Cluster
   ↓
Driver + Executors
   ↓
Distributed Processing

Most important interview line:
In Databricks, compute provides the resources for running Spark workloads, with the driver coordinating execution and executors performing the distributed processing.