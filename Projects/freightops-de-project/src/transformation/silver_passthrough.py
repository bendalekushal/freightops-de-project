from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = SparkSession.builder\
    .appName("Passthrough")\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

tables_to_pass_through = {
    "loads": "data/raw/loads.csv",
    "drivers": "data/raw/drivers.csv",
    "facilities": "data/raw/facilities.csv",
    "routes": "data/raw/routes.csv",
    "maintenance_records": "data/raw/maintenance_records.csv",
    "safety_incidents": "data/raw/safety_incidents.csv",
    "delivery_events": "data/raw/delivery_events.csv",
    "trailers": "data/raw/trailers.csv",
    "driver_monthly_metrics": "data/raw/driver_monthly_metrics.csv",
    "truck_utilization_metrics": "data/raw/truck_utilization_metrics.csv",
}

for table_name, path in tables_to_pass_through.items():
    df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(path)
    df.write.format("delta").mode("overwrite").save(f"data/silver/{table_name}")
    print(f"{table_name}: {df.count()} rows written to Silver")

spark.stop()