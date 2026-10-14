Day 69 — Databricks Workspace + Notebooks + Magic Commands

Today we will go deeper into the practical Databricks notebook environment. Since Day 68 already covered the basic concepts, we won't repeat Spark architecture.

1. Day 69 Goal

By the end of Day 69, you should understand:

Databricks Workspace
        ↓
Notebook
        ↓
Cells
        ↓
Code execution
        ↓
Magic Commands
        ↓
Python / SQL / File commands

We will specifically practice:

Workspace navigation
Creating/opening notebooks
Notebook cells
Running cells
Adding/removing cells
Python cells
SQL cells
%python
%sql
%fs
%pip
Basic notebook organization
Practical interview questions
Part 1 — Databricks Workspace
2. What is a Workspace?

A Databricks Workspace is the environment where we organize and work with Databricks resources.

Think of it as the main working area of your Databricks project.

Databricks
    ↓
Workspace
    ├── Notebooks
    ├── Files
    ├── Folders
    └── Other resources

For Data Engineering, notebooks are one of the most commonly used resources.

3. Open Databricks

Open your Databricks Free Edition workspace.

You should see the Databricks interface with areas such as:

Workspace
Compute
SQL
Catalog / data-related areas
Recent items
Notebooks

The exact UI can change over time, so don't worry if your interface looks slightly different.

4. Create the Day 69 Notebook

Create a new notebook named:

Day69_Workspace_Notebooks

Use:

Python
5. What is a Notebook?

A notebook is an interactive environment where we write and execute code.

For example:

print("Day 69 - Databricks")

Run the cell.

Expected:

Day 69 - Databricks
6. What is a Cell?

A notebook is divided into cells.

Each cell can contain code or other content.

Example:

Notebook
   │
   ├── Cell 1 → Python
   │
   ├── Cell 2 → Python
   │
   ├── Cell 3 → SQL
   │
   └── Cell 4 → Markdown

This makes notebooks useful for interactive development.

7. Multiple Cells

Create another cell:

name = "Gyaneshwar"
print(name)

Then another:

age = 25
print(age)

The cells are executed independently, but variables created by earlier cells can generally be used by later cells during the same notebook session.

Example:

name = "Gyaneshwar"

Then:

print(name)

Output:

Gyaneshwar
8. Cell Execution Order

Notebooks do not automatically guarantee that you executed cells from top to bottom.

For example:

Cell 1
name = "Gyaneshwar"

Cell 2
print(name)

works if Cell 1 has already been executed.

But if you execute Cell 2 before Cell 1, the variable may not exist.

Therefore, when developing notebooks:

Keep the logical execution order clear.

9. Python in Databricks

A Python notebook can directly execute Python code.

Example:

x = 10
y = 20

print(x + y)

Output:

30

We will mainly use Python/PySpark for our Data Engineering work.

10. Spark is Already Available

In Databricks, we generally don't need to manually create a SparkSession.

We can directly use:

spark

For example:

print(spark.version)

And:

df = spark.createDataFrame(
    [(1, "Rahul"), (2, "Priya")],
    ["id", "name"]
)

df.show()
Part 2 — Magic Commands
11. What are Magic Commands?

Databricks provides special commands called magic commands.

They start with:

%

They allow us to perform special operations inside notebooks.

Some important ones are:

%python
%sql
%fs
%pip
12. %python

%python tells Databricks that the cell should be interpreted as Python.

Example:

%python

print("Hello from Python")

Output:

Hello from Python

In a Python notebook, you normally don't need %python for every Python cell because Python is already the notebook's default language.

13. %sql

%sql allows us to execute SQL in a notebook.

Example:

%sql

SELECT 1 AS number;

Expected:

+------+
|number|
+------+
|     1|
+------+

This is extremely useful because Data Engineers commonly use both:

PySpark
+
SQL
14. Python + SQL in the Same Notebook

A very useful Databricks feature is that we can work with multiple languages in the same notebook.

For example:

Cell 1
data = [
    (1, "Rahul", "Hyderabad"),
    (2, "Priya", "Bangalore"),
    (3, "Amit", "Chennai")
]

df = spark.createDataFrame(
    data,
    ["id", "name", "city"]
)

df.show()
Cell 2
%sql

SELECT 1 AS test;

So one notebook can contain different types of cells.

15. %fs

%fs stands for filesystem-related commands.

It is commonly used to interact with files available through Databricks filesystem interfaces.

Example:

%fs ls

Depending on your current environment and available files, this may show directories/files.

You can also specify a path:

%fs ls /FileStore

The exact available paths can vary in Databricks environments.

16. %fs vs Python File Operations

Don't confuse these.

Python
import os

This works with the filesystem visible to Python.

%fs
%fs ls

This is a Databricks filesystem command.

For our roadmap, the important idea is:

%fs provides a convenient Databricks notebook interface for working with filesystem paths.

Later, when we work with Azure Data Lake, we will work with cloud storage paths as well.

17. %pip

%pip is used to install Python packages in a Databricks environment.

Example:

%pip install pandas

Or:

%pip install requests

After installing a package, Databricks may require the Python environment to restart depending on the package/environment.

Important

Don't randomly install packages.

Only install a package when the project actually needs it.

18. Important Magic Commands

Remember these:

Magic Command	Purpose
%python	Execute Python
%sql	Execute SQL
%fs	Work with filesystem paths
%pip	Install Python packages

The four are enough for our current roadmap.

Part 3 — Notebook Markdown
19. Why Use Markdown?

A notebook isn't only for code.

We can also document what the code is doing.

Example:

# Customer Data Processing

This notebook reads customer data
and performs basic transformations.

This helps other engineers understand the notebook.

20. Notebook Structure

A clean Data Engineering notebook can look like:

# Customer Pipeline

## 1. Configuration
    ↓
## 2. Read Data
    ↓
## 3. Validate Data
    ↓
## 4. Transform Data
    ↓
## 5. Write Data
    ↓
## 6. Validation

This is much better than putting hundreds of random cells together.

Part 4 — Practical Exercise

Now let's create a small notebook.

21. Cell 1 — Notebook Title

Create a Markdown cell:

# Day 69 - Databricks Workspace and Notebooks
22. Cell 2 — Python
print("Databricks Day 69")

Expected:

Databricks Day 69
23. Cell 3 — Spark Version
print("Spark Version:", spark.version)
24. Cell 4 — Create DataFrame
data = [
    (1, "Rahul", "Hyderabad"),
    (2, "Priya", "Bangalore"),
    (3, "Amit", "Chennai"),
    (4, "Neha", "Pune")
]

columns = ["customer_id", "name", "city"]

df = spark.createDataFrame(data, columns)

df.show()
25. Cell 5 — Schema
df.printSchema()
26. Cell 6 — PySpark Transformation
hyderabad_df = df.filter(
    df.city == "Hyderabad"
)

hyderabad_df.show()

Expected:

+-----------+-----+---------+
|customer_id| name|     city|
+-----------+-----+---------+
|          1|Rahul|Hyderabad|
+-----------+-----+---------+
Part 5 — SQL Practice
27. Create a Temporary View

Run Python:

df.createOrReplaceTempView("customers")

This creates a temporary SQL view.

28. Query Using %sql

Create a new cell:

%sql

SELECT *
FROM customers;

You should see the customer data.

29. SQL Filtering

Run:

%sql

SELECT *
FROM customers
WHERE city = 'Hyderabad';

Expected:

Rahul
Hyderabad
30. SQL Aggregation

Run:

%sql

SELECT city, COUNT(*) AS customer_count
FROM customers
GROUP BY city;

This demonstrates how PySpark-created data can be queried using SQL.

Part 6 — Understanding the Flow

The complete flow is:

Python
   ↓
Create Spark DataFrame
   ↓
Temporary View
   ↓
%sql
   ↓
SQL Query

This is one of the useful features of Databricks notebooks.

Part 7 — Practical %fs Exercise

Run:

%fs ls

Observe the result.

The output depends on what files/directories are available in your workspace.

The important thing is understanding the command:

%fs

means filesystem-related Databricks operations.

Part 8 — Practical %pip Understanding

You don't need to install anything just for the sake of installation.

For understanding, remember:

%pip install package_name

Example:

%pip install requests

Then Python can use the installed package:

import requests

Again, don't install unnecessary packages during this roadmap.

Part 9 — Notebook Execution

A typical notebook execution pattern is:

Read / Configure
      ↓
Load Data
      ↓
Validate
      ↓
Transform
      ↓
Write
      ↓
Validate Output

Later, this will become our actual Databricks pipeline.

Part 10 — Common Mistakes
Mistake 1 — Running cells in the wrong order

Example:

print(df.count())

before creating df.

This can cause an error.

Solution

Execute the required setup cells first.

Mistake 2 — Forgetting %sql

If the notebook's default language is Python:

SELECT * FROM customers;

will not be interpreted as SQL.

Use:

%sql

SELECT * FROM customers;
Mistake 3 — Thinking %fs is normal Python

This:

%fs ls

is a Databricks magic command, not Python syntax.

Mistake 4 — Installing packages unnecessarily

Don't do:

%pip install everything

Install only what your workload requires.

Part 11 — Interview Questions
Q1. What are Databricks magic commands?

Answer:

Magic commands are special commands beginning with % that provide additional notebook functionality, such as executing SQL, interacting with files, or installing Python packages.

Q2. What is %sql?

Answer:

%sql allows us to execute SQL statements inside a Databricks notebook.

Q3. What is %fs?

Answer:

%fs provides Databricks notebook commands for interacting with filesystem paths.

Q4. What is %pip?

Answer:

%pip is used to install Python packages in the Databricks environment.

Q5. Can Python and SQL be used in the same Databricks notebook?

Answer:

Yes. Databricks supports multiple languages in notebooks using magic commands such as %python and %sql.

Q6. Why are notebooks useful for Data Engineers?

Answer:

Notebooks provide an interactive environment where Data Engineers can develop, test, debug, document, and execute data processing code using PySpark and SQL.

Q7. What is a temporary view?

Answer:

A temporary view exposes a DataFrame as a SQL view so that we can query the DataFrame using Spark SQL.

Example:

df.createOrReplaceTempView("customers")

Then:

%sql

SELECT *
FROM customers;
Part 12 — Real-World Usage

In a real Data Engineering project, a notebook might contain:

Databricks Notebook
        │
        ├── Read configuration
        │
        ├── Read data from ADLS
        │
        ├── Validate data
        │
        ├── PySpark transformations
        │
        ├── SQL transformations
        │s
        ├── Write Delta table
        │
        └── Validate output

Later, the notebook can be executed through a:

Databricks Job

and eventually become part of a production workflow.