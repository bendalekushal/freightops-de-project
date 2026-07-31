from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = SparkSession.builder\
    .appName("SchemaCheck")\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

tables_to_check = {
    "delivery_events": "data/raw/delivery_events.csv",
    "drivers": "data/raw/drivers.csv",
    "fuel_purchases": "data/raw/fuel_purchases.csv",
    "loads": "data/raw/loads.csv",
    "maintenance_records": "data/raw/maintenance_records.csv",
    "safety_incidents": "data/raw/safety_incidents.csv",
    "trailers": "data/raw/trailers.csv",
    "trucks": "data/raw/trucks.csv",
}

for table_name, path in tables_to_check.items():
    df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(path)
    print(f"--- {table_name} ---")
    df.printSchema()

spark.stop()