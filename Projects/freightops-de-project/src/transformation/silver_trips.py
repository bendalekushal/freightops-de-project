from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col
from delta import configure_spark_with_delta_pip

builder = SparkSession.builder\
    .appName("SilverTrips")\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

trips_df = spark.read.format("csv")\
    .option("header", "true")\
    .option("inferSchema", "true")\
    .load("data/raw/trips.csv")

print("BEFORE:")
trips_df.printSchema()

trips_df = trips_df.withColumn\
    ("driver_id_missing", when(col("driver_id").isNull(), True).otherwise(False))
trips_df = trips_df.withColumn\
    ("trailer_id_missing", when(col("trailer_id").isNull(), True).otherwise(False))
trips_df = trips_df.withColumn\
    ("truck_id_missing", when(col("truck_id").isNull(), True).otherwise(False))

missing_drivers_count = trips_df.filter(col("driver_id_missing") == True).count()
print("driver_id missing count:", missing_drivers_count)

missing_trailers_count = trips_df.filter(col("trailer_id_missing") == True).count()
print("trailer_id missing count:", missing_trailers_count)

missing_trucks_count = trips_df.filter(col("truck_id_missing") == True).count()
print("truck_id missing count:", missing_trucks_count)

print("AFTER:")
trips_df.printSchema() 

trips_df.write\
    .format("delta")\
    .mode("overwrite")\
    .save("data/silver/trips")

trips_df.show()

spark.stop()
