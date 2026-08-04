from pyspark.sql import SparkSession
from pyspark.sql.functions import sum

spark=(
	SparkSession.builder
	.appName("Day60_Complete_ETL")
	.master("local[*]")
	.getOrCreate()
)

customers=(
	spark.read
	.option("header", True)
    	.option("inferSchema", True)
	.csv("data/customers.csv")
)

orders = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/orders.csv")
)

# -----------------------------
# Transform
# -----------------------------
joined_df=(
	customers.join(orders,on="customer_id",how="inner")
)

sales_report=(
	joined_df.groupby("customer_id", "name","city")
	.agg(sum("amount").alias("total_sales"))
)


# -----------------------------
# Load
# -----------------------------

sales_report.write.mode("overwrite").option("header",True).csv("output/sales_report")

print("=" * 50)
print("Sales Report")
print("=" * 50)

sales_report.show()

spark.stop()



















