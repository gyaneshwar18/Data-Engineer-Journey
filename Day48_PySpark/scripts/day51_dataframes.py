from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

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

print("=" *50)
print("Selecting columns:")
print("=" *50)

df.select("customer_id", "name").show()

print("=" *50)
print("Adding Filtering:")
print("=" *50)

df.filter(df.age>27).show()

print("=" *50)
print("Adding columns:")
print("=" *50)

df.withColumn("Country", lit("India")).show()


spark.stop()
