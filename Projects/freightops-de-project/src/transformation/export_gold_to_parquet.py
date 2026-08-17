from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = SparkSession.builder\
    .appName("ExportGoldToParquet")\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

tables_to_pass_through = {
    "fact_trips": "data/gold/fact_trips",
    "dim_driver": "data/gold/dim_driver",
    "dim_truck": "data/gold/dim_truck",
    "dim_customer": "data/gold/dim_customer",
    "dim_route": "data/gold/dim_route",
    "dim_trailer": "data/gold/dim_trailer",
}

for table_name, path in tables_to_pass_through.items():
    df = spark.read.format("delta").load(path)
    df.write.format("parquet").mode("overwrite").save(f"data/gold_parquet/{table_name}")
    print(f"{table_name}: {df.count()} rows written to Gold Parquet")

spark.stop()