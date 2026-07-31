from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from delta import configure_spark_with_delta_pip

builder = SparkSession.builder\
    .appName("GoldRevenuePerMile")\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

customers_df = spark.read.format("delta")\
    .option("header", "true")\
    .option("inferSchema", "true")\
    .load("data/silver/customers")

loads_df = spark.read.format("delta")\
    .option("header", "true")\
    .option("inferSchema", "true")\
    .load("data/silver/loads")

trips_df = spark.read.format("delta")\
    .option("header", "true")\
    .option("inferSchema", "true")\
    .load("data/silver/trips")


joined_df = loads_df.join(F.broadcast(customers_df), on="customer_id", how="inner")\
    .join(trips_df, on="load_id", how="inner")

result_df = joined_df.groupBy("customer_id").agg(
   F.round(F.sum("revenue"), 2).alias("total_revenue"),
    F.round(F.sum("actual_distance_miles"), 2).alias("total_miles")
)
result_df = result_df.withColumn(
    "revenue_per_mile", 
    F.round(F.col("total_revenue") / F.col("total_miles"), 2)
)

result_df = result_df.orderBy(F.col("revenue_per_mile").desc())

result_df.show(10)