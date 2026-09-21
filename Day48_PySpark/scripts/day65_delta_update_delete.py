from utils.spark_session import create_spark_session
from delta.tables import DeltaTable

# create Spark Session

spark= create_spark_session("Day65_deltaUpdateandDelete")


# Delta Table Path 

delta_path="output/delta/day62_sales"

#load Delta Table 

delta_table=DeltaTable.forPath(
	spark,
	delta_path
)

# show Current data

print("before Update")

delta_table.toDF().show()

# update 

delta_table.update(
	condition="order_id=1000",
	set={
		"amount":"8000"
	}
)

print("after Update")

delta_table.toDF().show()


# delete

delta_table.delete(
	condition="order_id=1000"
)

print("after delete")

delta_table.toDF().show()

# show delta History

print("Delta Table History")

delta_table.history().show(truncate=False)

spark.stop()
























