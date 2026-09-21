from utils.spark_session import create_spark_session
from pyspark.sql import Row
from pyspark.sql.functions import col


# ---------------------------------------
# Create Spark Session
# ---------------------------------------

spark = create_spark_session("Day63_DeltaACID")


# ---------------------------------------
# Delta Table Path
# ---------------------------------------

delta_path = "output/delta/day62_sales"


# ---------------------------------------
# Read Current Delta Table
# ---------------------------------------

delta_df = (
    spark.read
    .format("delta")
    .load(delta_path)
)

print("=" * 50)
print("Current Delta Table")
print("=" * 50)

delta_df.show()

print("=" * 50)
print("Current Schema")
print("=" * 50)

delta_df.printSchema()


# ---------------------------------------
# Add New Data
# ---------------------------------------

new_sales = spark.createDataFrame([
    Row(
        order_id=1000,
        customer="ACID_Test",
        city="Hyderabad",
        amount=7000
    )
])


# ---------------------------------------
# Match Existing Delta Schema
# ---------------------------------------

new_sales = (
    new_sales
    .withColumn("order_id", col("order_id").cast("integer"))
    .withColumn("amount", col("amount").cast("integer"))
)


print("=" * 50)
print("New Data")
print("=" * 50)

new_sales.show()

print("=" * 50)
print("New Data Schema")
print("=" * 50)

new_sales.printSchema()


# ---------------------------------------
# Append New Data to Delta
# ---------------------------------------

(
    new_sales.write
    .format("delta")
    .mode("append")
    .save(delta_path)
)

print("=" * 50)
print("Transaction Completed Successfully")
print("=" * 50)


# ---------------------------------------
# Read Delta Table Again
# ---------------------------------------

updated_df = (
    spark.read
    .format("delta")
    .load(delta_path)
)

print("=" * 50)
print("Updated Delta Table")
print("=" * 50)

updated_df.show()


# ---------------------------------------
# Stop Spark
# ---------------------------------------

spark.stop()
