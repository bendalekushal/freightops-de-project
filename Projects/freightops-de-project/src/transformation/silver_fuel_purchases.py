from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col
from delta import configure_spark_with_delta_pip

builder = SparkSession.builder\
    .appName("SilverFuelPurchases")\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

fuel_purchases_df = spark.read.format("csv")\
    .option("header", "true")\
    .option("inferSchema", "true")\
    .load("data/raw/fuel_purchases.csv")

print("BEFORE:")
fuel_purchases_df.printSchema()

fuel_purchases_df = fuel_purchases_df.withColumn\
    ("driver_id_missing", when(col("driver_id").isNull(), True).otherwise(False))

missing_drivers_count = fuel_purchases_df.filter(col("driver_id_missing") == True).count()
print("driver_id missing count:", missing_drivers_count)

print("AFTER:")
fuel_purchases_df.printSchema()

fuel_purchases_df.write\
    .format("delta")\
    .mode("overwrite")\
    .save("data/silver/fuel_purchases")

fuel_purchases_df.show(5)

spark.stop()