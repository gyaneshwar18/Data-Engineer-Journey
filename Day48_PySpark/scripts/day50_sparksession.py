from pyspark.sql import SparkSession

spark= (
	SparkSession.builder
	.appName("Day50_SparkSession")
	.master("local[*]")
	.getOrCreate()
)

print("="*50)
print("Spark version: ", spark.version)

print("="*50)
print("Spark context: ", spark.sparkContext)

print("="*50)
print("Application name: ", spark.sparkContext.appName)

print("="*50)
print("Master: ", spark.sparkContext.master)


spark.stop()
