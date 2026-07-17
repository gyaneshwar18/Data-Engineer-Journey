from pyspark.sql import SparkSession
from pyspark.sql.functions import sum,avg,count,max,min

spark=(
	SparkSession.builder
	.appName("day53_aggregations")
	.master("local[*]")
	.getOrCreate()
)


df=(
	spark.read
	.option("header",True)
	.option("inferschema",True)
	.csv("data/sales.csv")
)

print("=" * 50)
print("Original Data")
print("=" * 50)

df.show()

print("=" * 50)
print("Total Sales by City")
print("=" * 50)

df.groupby("city").sum("amount").show()

print("=" * 50)
print("Business Metrics")
print("=" * 50)


df.groupby("city").agg(
	sum("amount").alias("Total_Sales"),
	avg("amount").alias("Avg_Sales"),
	count("order_id").alias("Total_Orders"),
	max("amount").alias("Highest_sale"),
	min("amount").alias("Lowest_sale")
).show()

spark.stop()



