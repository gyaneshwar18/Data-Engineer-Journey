from pyspark.sql import SparkSession

spark=(
	SparkSession.builder
	.appName("Day55_SparkSQL")
	.master("local[*]")
	.getOrCreate()
)

df=(
	spark.read
	.option("header",True)
	.option("inferSchema",True)
	.csv("data/customers.csv")
)

print("=" * 50)
print("Original DataFrame")
print("=" * 50)

df.show()

# Create Temporary View
df.createOrReplaceTempView("customers")

print("=" * 50)
print("Spark sql")
print("=" * 50)

result=spark.sql("""
	SELECT *
	FROM customers"""
)

result.show()

spark.stop()


