from utils.spark_session import create_spark_session
from pyspark.sql import Row


# ---------------------------------------
# Create Spark Session
# ---------------------------------------

spark = create_spark_session("Day67_Schema")


# ---------------------------------------
# Delta Table Path
# ---------------------------------------

delta_path = "output/delta/day62_sales"


# ---------------------------------------
# Read Existing Delta Table
# ---------------------------------------

delta_df = (
    spark.read
    .format("delta")
    .load(delta_path)
)


print("=" * 60)
print("CURRENT DELTA TABLE")
print("=" * 60)

delta_df.show()

print("=" * 60)
print("CURRENT SCHEMA")
print("=" * 60)

delta_df.printSchema()


# ---------------------------------------
# Create Compatible Data
# ---------------------------------------
schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("customer", StringType(), True),
    StructField("city", StringType(), True),
    StructField("amount", IntegerType(), True)
])

compatible_data = spark.createDataFrame([
    (2000, "Schema_Test", "Hyderabad", 5000)
], schema=schema)


print("=" * 60)
print("COMPATIBLE DATA")
print("=" * 60)

compatible_data.show()


# ---------------------------------------
# Append Compatible Data
# ---------------------------------------

compatible_data.write \
    .format("delta") \
    .mode("append") \
    .save(delta_path)


print("=" * 60)
print("COMPATIBLE DATA INSERTED")
print("=" * 60)


# ---------------------------------------
# Create New Column
# ---------------------------------------

new_column_data = spark.createDataFrame([
    Row(
        order_id=2001,
        customer="Evolution_Test",
        city="Hyderabad",
        amount=6000,
        discount=500
    )
])


print("=" * 60)
print("DATA WITH NEW COLUMN")
print("=" * 60)

new_column_data.show()

new_column_data.printSchema()


# ---------------------------------------
# Schema Evolution
# ---------------------------------------

new_column_data.write \
    .format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save(delta_path)


print("=" * 60)
print("SCHEMA EVOLUTION COMPLETED")
print("=" * 60)


# ---------------------------------------
# Read Final Table
# ---------------------------------------

final_df = (
    spark.read
    .format("delta")
    .load(delta_path)
)


print("=" * 60)
print("FINAL DELTA TABLE")
print("=" * 60)

final_df.show()

print("=" * 60)
print("FINAL SCHEMA")
print("=" * 60)

final_df.printSchema()


# ---------------------------------------
# Stop Spark
# ---------------------------------------

spark.stop()
