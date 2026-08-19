from utils.spark_session import create_spark_session
from pyspark.sql import Row
from pyspark.sql.functions import col


# ---------------------------------------
# Create Spark Session
# ---------------------------------------

spark = create_spark_session("Day62_DeltaReadWrite")


# ---------------------------------------
# Read Source CSV
# ---------------------------------------

sales_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/sales.csv")
)

print("=" * 50)
print("Source CSV Data")
print("=" * 50)

sales_df.show()


# ---------------------------------------
# Write DataFrame as Delta
# ---------------------------------------

delta_path = "output/delta/day62_sales"

(
    sales_df.write
    .format("delta")
    .mode("overwrite")
    .save(delta_path)
)

print("=" * 50)
print("Delta Table Written Successfully")
print("=" * 50)


# ---------------------------------------
# Read Delta Table
# ---------------------------------------

delta_df = (
    spark.read
    .format("delta")
    .load(delta_path)
)

print("=" * 50)
print("Data Read From Delta")
print("=" * 50)

delta_df.show()


# ---------------------------------------
# Display Schema
# ---------------------------------------

print("=" * 50)
print("Delta Table Schema")
print("=" * 50)

delta_df.printSchema()


# ---------------------------------------
# Create New Sales Record
# ---------------------------------------

new_sales = spark.createDataFrame([
    Row(
        order_id=999,
        customer="Test",
        city="Hyderabad",
        amount=5000
    )
])


# ---------------------------------------
# Match Existing Schema
# ---------------------------------------

new_sales = (
    new_sales
    .withColumn("order_id", col("order_id").cast("integer"))
    .withColumn("amount", col("amount").cast("integer"))
)


# ---------------------------------------
# Append New Record to Delta Table
# ---------------------------------------

(
    new_sales.write
    .format("delta")
    .mode("append")
    .save(delta_path)
)

print("=" * 50)
print("New Record Appended Successfully")
print("=" * 50)


# ---------------------------------------
# Read Updated Delta Table
# ---------------------------------------

delta_df = (
    spark.read
    .format("delta")
    .load(delta_path)
)

print("=" * 50)
print("Updated Delta Table")
print("=" * 50)

delta_df.show()


# ---------------------------------------
# Stop Spark
# ---------------------------------------

spark.stop()

print("=" * 50)
print("Spark Session Stopped")
print("=" * 50)
