from utils.spark_session import create_spark_session
from pyspark.sql.functions import col

#create Spark session

spark= create_spark_session("Day68_DeltaETL")

# Source Paths

sales_path="data/sales.csv"
customers_path="data/customers.csv"

# delta path

bronze_path="output/delta/day68_bronze_sales"
silver_path="output/delta/day68_silver_sales"

# Read Source data

sales_df= (
	spark.read
	.option("header",True)
	.option("inferSchema", True)
	.csv(sales_path)
)

customers_df=(
	spark.read
	.option("header", True)
	.option("inferSchema", True)
	.csv(customers_path)
)

sales_df.show()
customers_df.show()

# BRonze Layer

sales_df.write.format("delta").mode("overwrite").save(bronze_path)


print("Bronze table created")


# Transformations

silver_df=(
	sales_df.filter(col("amount")>0)
)
print("Tranformed")

silver_df.show()

# silver Delta Table

(
	silver_df.write	
	.format("delta")
	.mode("overwrite")
	.save(silver_path)
)

# Read silver Table

final_df=(
	spark.read
	.format("delta")
	.load(silver_path)
)

final_df.show()

spark.stop()

















































