from pyspark.sql import SparkSession

spark=(
	SparkSession.builder
	.appName("")
	.master("local[*]")
	.getOrCreate()
)


print("=" * 50)
print("Spark Version")
print("=" * 50)

print(spark.version)

spark.stop()


