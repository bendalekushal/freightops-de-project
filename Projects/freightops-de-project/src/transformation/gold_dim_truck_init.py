from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from delta import configure_spark_with_delta_pip

builder = SparkSession.builder\
    .appName("DimTruckInit")\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

trucks_df = spark.read.format("delta").load("data/silver/trucks")


dim_truck_df = trucks_df \
    .withColumn("effective_start_date", F.current_date()) \
    .withColumn("effective_end_date", F.lit(None).cast("date")) \
    .withColumn("is_current", F.lit(True))

dim_truck_df.write.format("delta").mode("overwrite").save("data/gold/dim_truck")

dim_truck_df.printSchema()

dim_truck_df.show(5)

spark.stop()