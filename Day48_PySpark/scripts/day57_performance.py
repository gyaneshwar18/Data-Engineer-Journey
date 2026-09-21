from pyspark.sql import SparkSession

spark= (
	SparkSession.builder
	.appName("Day57_Performance")
	.master("local[*]")
	.getOrCreate()

)

df=(
	spark.read
	.option("header",True)
	.option("inferSchema",True)
	.csv("data/customers.csv")
)

filtered_df= df.filter(df.age>25)

print("=" * 50)
print("Caching DataFrame")
print("=" * 50)

filtered_df.persist()
filtered_df.cache()
filtered_df.explain()

print("First Action")
filtered_df.show()


print("Second Action")
count = filtered_df.count()
print(f"Count: {count}")


spark.stop()
