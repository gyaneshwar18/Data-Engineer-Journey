from utils.spark_session import create_spark_session


# ---------------------------------------
# Create Spark Session
# ---------------------------------------

spark = create_spark_session("Day61_DeltaLake")


# ---------------------------------------
# Display Spark Version
# ---------------------------------------

print("=" * 50)
print("Spark Information")
print("=" * 50)

print("Spark Version:", spark.version)


# ---------------------------------------
# Extract
# ---------------------------------------

sales_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/sales.csv")
)


print("=" * 50)
print("Source Data")
print("=" * 50)

sales_df.show()


# ---------------------------------------
# Write DataFrame as Delta Table
# ---------------------------------------

sales_df.write \
    .format("delta") \
    .mode("overwrite") \
    .save("output/delta/sales")


print("=" * 50)
print("Delta Table Created Successfully")
print("=" * 50)


# ---------------------------------------
# Read Delta Table
# ---------------------------------------

delta_df = (
    spark.read
    .format("delta")
    .load("output/delta/sales")
)


print("=" * 50)
print("Data Read From Delta Table")
print("=" * 50)

delta_df.show()


# ---------------------------------------
# Stop Spark
# ---------------------------------------

spark.stop()

print("=" * 50)
print("Spark Session Stopped")
print("=" * 50)
