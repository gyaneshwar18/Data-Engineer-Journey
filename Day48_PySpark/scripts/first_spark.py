from pyspark.sql import SparkSession

# Create SparkSession
spark = (
    SparkSession.builder
    .appName("Day49_FirstSparkApp")
    .master("local[*]")
    .getOrCreate()
)

print("✅ SparkSession Created Successfully!")

print("Spark Version:", spark.version)

spark.stop()

print("SparkSession Stopped.")
