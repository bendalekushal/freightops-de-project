from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, col
from delta import configure_spark_with_delta_pip

builder = SparkSession.builder\
    .appName("SilverTrucks")\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

trucks_df = spark.read.format("csv")\
    .option("header", "true")\
    .option("inferSchema", "true")\
    .load("data/raw/trucks.csv")

print("BEFORE:")
trucks_df.printSchema()

trucks_df = trucks_df\
    .withColumn("acquisition_date", to_date(col("acquisition_date"), "dd-MM-yyyy"))

print("AFTER:")
trucks_df.printSchema()

trucks_df.write\
    .format("delta")\
    .mode("overwrite")\
    .save("data/silver/trucks")

trucks_df.show()

spark.stop()