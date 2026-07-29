from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, col
from delta import configure_spark_with_delta_pip

builder = SparkSession.builder\
    .appName("SilverCustomers")\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

customers_df = spark.read.format("csv")\
    .option("header", "true")\
    .option("inferSchema", "true")\
    .load("data/raw/customers.csv")

print("BEFORE:")
customers_df.printSchema()

customers_df = customers_df\
    .withColumn("contract_start_date", to_date(col("contract_start_date"), "dd-MM-yyyy"))

print("AFTER:")
customers_df.printSchema()

customers_df.write\
    .format("delta")\
    .mode("overwrite")\
    .save("data/silver/customers")

customers_df.show()

spark.stop()