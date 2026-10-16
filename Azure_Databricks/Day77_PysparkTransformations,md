Day 77 — PySpark Transformations in Azure Databricks

90-Day Data Engineering Journey | Hands-on + Interview Preparation

Today, we'll learn how to transform data using PySpark in Azure Databricks.

We'll use your existing ADLS Gen2 dataset, source/Sales.csv, and keep everything aligned with your locked roadmap.

Today's approach: Complete lesson in one response, organized into separate notebooks for readability. Run the notebooks in order and share any errors if you encounter them.

1. Concept — What, Why, and Where?
What are PySpark transformations?

Transformations are operations used to modify, filter, or select data in a Spark DataFrame.

For example, a company might receive a sales dataset containing thousands or millions of records. The Data Engineer may need to:

Select specific columns.
Filter products by category.
Create a new column.
Remove unnecessary columns.

PySpark provides transformations to perform these operations.

Where do transformations fit in a data pipeline?
ADLS Gen2
    |
    | Sales.csv
    v
Azure Databricks
    |
    | Read using PySpark
    v
Source DataFrame
    |
    | Transformations
    |   - select()
    |   - filter()
    |   - withColumn()
    v
Transformed DataFrame
    |
    | Write
    v
ADLS Gen2 / Destination
Today's learning objectives
Transformation	Purpose
select()	Select specific columns
filter()	Keep rows matching a condition
withColumn()	Create or modify a column
drop()	Remove a column
distinct()	Retrieve distinct rows
orderBy()	Sort rows

We'll practice these operations using your existing Sales dataset.

2. Hands-on Setup — Your Existing Environment

We'll continue using your configured Azure Databricks environment.

Source:

source_path = "abfss://source@datalakegyan.dfs.core.windows.net/Sales.csv"

Destination:

destination_path = "abfss://destination@datalakegyan.dfs.core.windows.net/sales.csv"

We'll load the source dataset into a DataFrame.

Important: Today's transformation exercises will not overwrite your existing destination output. We'll use the existing source data for our exercises and write the final result to a separate path within your existing destination container.

3. Step-by-Step Coding

We'll organize today's practical work into three notebooks.

Notebook 1: 01_basic_transformations
Task 1 — Read the Sales dataset

What are we doing?

Reading the existing CSV file into a DataFrame.

source_path = "abfss://source@datalakegyan.dfs.core.windows.net/Sales.csv"

sales_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(source_path)

display(sales_df)

Expected output: Your sales data should appear in a Databricks table.

The dataset contains columns such as Item_Identifier, Item_Type, Item_MRP, and Item_Outlet_Sales.

Task 2 — Select specific columns using select()

Concept

Sometimes, we don't need every column from the source dataset.

For example, if we're analyzing sales, we may need only the product type, price, and sales amount.

Code

selected_df = sales_df.select(
    "Item_Identifier",
    "Item_Type",
    "Item_MRP",
    "Item_Outlet_Sales"
)

display(selected_df)

Expected output

Item_Identifier	Item_Type	Item_MRP	Item_Outlet_Sales
Example product ID	Example category	Example price	Example sales

These values are illustrative; your actual output will contain your source records.

Explanation

select() returns a DataFrame containing only the specified columns.

It doesn't modify the original sales_df DataFrame.

Interview question: What is the purpose of select() in PySpark?

Answer: select() retrieves specific columns from a DataFrame, making it easier to work with the fields required for a particular task.

Task 3 — Filter rows using filter()

Concept

Filtering means selecting only the rows that satisfy a condition.

Suppose the business wants to analyze only products belonging to the Dairy category.

Code

dairy_df = sales_df.filter(
    sales_df.Item_Type == "Dairy"
)

display(dairy_df)

Expected output

Only records whose Item_Type equals Dairy should appear.

Explanation

sales_df.Item_Type == "Dairy"

Creates a condition that Spark evaluates for each row.

filter() returns the rows that satisfy that condition.

Interview question: What is the difference between select() and filter()?

Answer:

select() chooses columns.
filter() chooses rows.

Twisted question: Does filter() change the original DataFrame?

Answer: No. It returns a new DataFrame representing the filtered result. The original DataFrame remains unchanged.

Notebook 2: 02_column_transformations
Task 4 — Create a new column using withColumn()

Concept

Businesses often need derived columns for analysis.

For example, we can calculate a new sales classification based on Item_Outlet_Sales.

We'll classify sales values as High or Normal using a simple threshold of 1,000.

Code

from pyspark.sql.functions import when, col

classified_df = sales_df.withColumn(
    "Sales_Category",
    when(col("Item_Outlet_Sales") > 1000, "High")
    .otherwise("Normal")
)

display(classified_df)

Expected output

The DataFrame will contain a new column named Sales_Category.

Item_Outlet_Sales	Sales_Category
1500.0	High
800.0	Normal
2500.0	High

These are illustrative examples, not actual records from your dataset.

Explanation

withColumn() creates or replaces a column.
when() evaluates a condition.
otherwise() specifies the result when the condition is false or not satisfied.

Important: The threshold of 1,000 is just a learning example, not a business-defined rule.

Interview question: What is withColumn() used for?

Answer: withColumn() creates a new column or replaces an existing column in a DataFrame.

Twisted question: What happens if the column already exists?

Answer: withColumn() replaces the existing column with the new expression's result.

Task 5 — Remove a column using `drop()

Day 77 — Task 5: Remove a Column Using drop()
1. Concept

The PySpark drop() transformation removes one or more columns from a DataFrame.

Why do we use it?

Remove unnecessary columns.
Keep only relevant information for downstream processing.
Simplify a DataFrame before writing or analyzing data.
2. Hands-on Coding

We'll use your existing sales_df DataFrame containing data from source/Sales.csv.

Code:

dropped_df = sales_df.drop("Item_Weight")

display(dropped_df)
3. Expected Output

The DataFrame will contain the original columns except Item_Weight.

For example:

Item_Identifier
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

The remaining columns should retain their original values.

4. Verify the Result

Run:

print("Original columns:", len(sales_df.columns))
print("Updated columns:", len(dropped_df.columns))

print("Item_Weight exists:", "Item_Weight" in dropped_df.columns)

Expected output:

Original columns: 12
Updated columns: 11
Item_Weight exists: False

These counts assume your source contains the 12 standard columns.

5. Important Point

drop() does not modify the original sales_df. It returns a new DataFrame.

display(sales_df)    # Original DataFrame
display(dropped_df)  # DataFrame without Item_Weight

Both DataFrames remain available.

6. Interview Questions

Q1. What is drop() in PySpark?

drop() removes specified columns from a DataFrame and returns a new DataFrame.

Q2. How do you remove multiple columns?

updated_df = sales_df.drop("Item_Weight", "Outlet_Size")

Q3. What happens if the specified column doesn't exist?

For a simple string column name, drop() generally returns the DataFrame unchanged if that column is absent.

Q4. Does drop() modify the original DataFrame?

No. It returns a new DataFrame.

Twisted question: If you remove a column using drop(), does Spark immediately process the entire dataset?

Not necessarily. Spark transformations are generally lazy. Execution occurs when an action requires the result.

Task 5 Checklist
 Removed Item_Weight.
 Displayed the updated DataFrame.
 Verified the column count.
 Confirmed that Item_Weight is absent.

Next: Day 77, Task 6 — distinct() to retrieve distinct rows.

From Day 78 onward, I'll follow your preferred order: concept explanations → practical notebooks and coding → interview questions and twisted questions at the end.