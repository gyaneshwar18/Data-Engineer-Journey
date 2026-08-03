from pyspark.sql import SparkSession
from pyspark.sql.functions import sum

spark = (
    SparkSession.builder
    .appName("Day59_Mini_ETL")
    .master("local[*]")
    .getOrCreate()
)

customers = (
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


df_join=customers.join(orders,on="customer_id", how="inner")


sales_report = (
    df_join
    .groupBy("customer_id", "name", "city")
    .agg(
        sum("amount").alias("total_sales")
    )
)

sales_report.show()

spark.stop()
