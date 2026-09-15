from utils.spark_session import create_spark_session
from delta.tables import DeltaTable

# create spark session 

spark=create_spark_session("day64_DeltaTimeTravel")


#Delta Table Path

delta_path="output/delta/day62_sales"


#Load Delta Table

delta_table= DeltaTable.forPath(
	spark,
	delta_path
)

# show Transaction History

print("="*50)
print("Delta Table History")
print("="*50)

delta_table.history().show(
	truncate=False
)

# Read Cuurent version

current_df=(
	spark.read
	.format("delta")
	.load(delta_path)
)


print("="*50)
print("current version")
print("="*50)

current_df.show()


#read version 0

version_0_df=(
	spark.read
	.format("delta")
	.option("versionAsOf",0)
	.load(delta_path)
)

print("="*50)
print("version 0")
print("="*50)

version_0_df.show()


spark.stop()




















