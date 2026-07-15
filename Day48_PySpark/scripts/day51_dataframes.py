from pyspark.sql import SparkSession

spark=(
	SparkSession.builder
	.appName("Day50_DataFrames")
	.master("local[*]")
	.getOrCreate()
)

df=(
	spark.read
	.option("header",True)
	.option("inferschema",True)
	.csv("data/customers.csv")
)

print("=" *50)
print("Showing data:")
print("=" *50)

df.show()
spark.stop()
