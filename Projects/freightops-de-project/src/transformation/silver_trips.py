from pyspark.sql import SparkSession
from pyspark.sql import functions as F 
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
    ("driver_id_missing", F.when(F.col("driver_id").isNull(), True).otherwise(False))
trips_df = trips_df.withColumn\
    ("trailer_id_missing", F.when(F.col("trailer_id").isNull(), True).otherwise(False))
trips_df = trips_df.withColumn\
    ("truck_id_missing", F.when(F.col("truck_id").isNull(), True).otherwise(False))

missing_drivers_count = trips_df.filter(F.col("driver_id_missing") == True).count()
print("driver_id missing count:", missing_drivers_count)

missing_trailers_count = trips_df.filter(F.col("trailer_id_missing") == True).count()
print("trailer_id missing count:", missing_trailers_count)

missing_trucks_count = trips_df.filter(F.col("truck_id_missing") == True).count()
print("truck_id missing count:", missing_trucks_count)

print("AFTER:")
trips_df.printSchema() 

trips_df.write\
    .format("delta")\
    .mode("overwrite")\
    .save("data/silver/trips")

print("Number of partitions:", trips_df.rdd.getNumPartitions())
trips_df.groupBy(F.spark_partition_id()).count().show()

skewed_df = trips_df.repartition(4, "trip_status")
skewed_df.groupBy(F.spark_partition_id()).count().show()
print("Skewed partitions:", skewed_df.rdd.getNumPartitions())


salted_df = trips_df.withColumn("salt", (F.rand() * 20).cast("int"))
salted_df = salted_df.repartition(4, "trip_status", "salt")
salted_df.groupBy(F.spark_partition_id()).count().show()
print("Salted partitions:", salted_df.rdd.getNumPartitions())

spark.stop()
