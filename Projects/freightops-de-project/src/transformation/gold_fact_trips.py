from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from delta import configure_spark_with_delta_pip

builder = SparkSession.builder\
    .appName("GoldFactTrips")\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

trips_df = spark.read.format("delta")\
    .option("header", "true")\
    .option("inferSchema", "true")\
    .load("data/silver/trips")

loads_df = spark.read.format("delta")\
    .option("header", "true")\
    .option("inferSchema", "true")\
    .load("data/silver/loads")

fact_trip_df = trips_df.join(loads_df, on="load_id", how="inner")\
    .select(
        "trip_id",
        "load_id",
        "driver_id",
        "truck_id",
        "trailer_id",
        "dispatch_date",
        "actual_distance_miles",
        "fuel_gallons_used",
        "average_mpg",
        "idle_time_hours",
        "driver_id_missing",
        "truck_id_missing",
        "trailer_id_missing",
        "customer_id",
        "route_id",
        "revenue",
        "fuel_surcharge"
    )

fact_trip_df.write\
    .format("delta")\
    .mode("overwrite")\
    .save("data/gold/fact_trips")

total_row_count = fact_trip_df.count()
print("Total row count in fact_trip_df:", total_row_count)

fact_trip_df.show(5)

spark.stop()