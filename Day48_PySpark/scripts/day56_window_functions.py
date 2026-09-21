from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import (
 row_number,
    rank,
    dense_rank,
    lag,
    lead,
    sum
)

spark= (
	SparkSession.builder
	.appName("Day56_WindowFunctions")
	.master("local[*]")
	.getOrCreate()
)

df=(
	spark.read
	.option("header",True)
	.option("inferSchema", True)
	.csv("data/employees.csv")
)

window_spec=Window.partitionBy("department").orderBy(df.salary.desc())

print("=" * 50)
print("ROW_NUMBER")
print("=" * 50)

df.withColumn("Row Number",row_number().over(window_spec)).show()

print("=" * 50)
print("RANK")
print("=" * 50)

df.withColumn(
    "rank",
    rank().over(window_spec)
).show()

print("=" * 50)
print("DENSE_RANK")
print("=" * 50)

df.withColumn(
    "dense_rank",
    dense_rank().over(window_spec)
).show()

print("=" * 50)
print("LAG")
print("=" * 50)

df.withColumn(
    "previous_salary",
    lag("salary").over(window_spec)
).show()

print("=" * 50)
print("LEAD")
print("=" * 50)

df.withColumn(
    "next_salary",
    lead("salary").over(window_spec)
).show()


print("=" * 50)
print("RUNNING TOTAL")
print("=" * 50)


running_window = (
    Window
    .partitionBy("department")
    .orderBy("salary")
)


df.withColumn(
    "running_total",
    sum("salary").over(running_window)
).show()
