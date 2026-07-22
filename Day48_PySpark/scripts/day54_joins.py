from pyspark.sql import SparkSession

spark=(
	SparkSession.builder
	.appName("Day54_Joins")
	.master("local[*]")
	.getOrCreate()
)

customers=(
	spark.read
	.option("header",True)
	.option("inferschema",True)
	.csv("data/customers.csv")
)

orders=(
        spark.read
        .option("header",True)
        .option("inferschema",True)
        .csv("data/orders.csv")
)

df_left=customers.join(orders, on="customer_id", how="left")
df_left.show()


df_right=customers.join(orders, on="customer_id", how="right")
df_right.show()

df_inner=customers.join(orders, on="customer_id", how="inner")
df_inner.show()

df_outer=customers.join(orders, on="customer_id", how="left")
df_outer.show()

spark.stop()
