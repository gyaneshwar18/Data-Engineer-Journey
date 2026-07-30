from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Day58_Partitioning")
    .master("local[*]")
    .getOrCreate()
)

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/customers.csv")
)

print("=" * 50)
print("Default Partitions")
print("=" * 50)

print(df.rdd.getNumPartitions())

df_repartition = df.repartition(4)

print(df_repartition.rdd.getNumPartitions())

df_coalesce = df_repartition.coalesce(2)

print(df_coalesce.rdd.getNumPartitions())

spark.stop()
