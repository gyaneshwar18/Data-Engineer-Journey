from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

spark = (
    SparkSession.builder
    .appName("Day52_Transformations")
    .master("local[*]")
    .getOrCreate()
)

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/customers.csv")
)

# Transformations
filtered_df= df.filter(df.age>25)

selected_df=filtered_df.select("name","city")

final_df=selected_df.withColumn("country",lit("India"))

print("Transformations Created!")

#Action
print("\nExecuting Action...\n")

final_df.show()

spark.stop()
