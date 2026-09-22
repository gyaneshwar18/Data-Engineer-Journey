from utils.spark_session import create_spark_session
from delta.tables import DeltaTable
from pyspark.sql import Row


#create spark session

spark=create_spark_session("Day66_DeltaMerge")

# ---------------------------------------
# Delta Table Path
# ---------------------------------------

delta_path = "output/delta/day62_sales"

# Delta Table Path

delta_table=DeltaTable.forPath(spark, delta_path)

# create source data

source_df= spark.createDataFrame([
	Row(
		order_id=2,
		customer="priya",
		city="Bangalore",
		amount=2500
	),
	Row(
		order_id=1001,
		customer="Merge_Test",
		city="Hyderabad",
		amount=9000
	)
])


# MERGE/UPSERT

(
	delta_table.alias("target")
	.merge(
		source_df.alias("source"),
		"target.order_id=source.order_id"
	)
	.whenMatchedUpdateAll()
	.whenNotMatchedInsertAll()
	.execute()
)

print("TARGET AFTER MERGE")
print("=" * 60)

delta_table.toDF().show()


print("Delta Table History")
delta_table.history().show(truncate=False)

spark.stop()


















