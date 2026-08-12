from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = SparkSession.builder\
    .appName("GoldRemainingDim")\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

tables_to_pass_through = {
    "dim_customer": "data/silver/customers",
    "dim_route": "data/silver/routes",
    "dim_trailer": "data/silver/trailers"
}

for table_name, path in tables_to_pass_through.items():
    df = spark.read.format("delta")\
        .load(path)
    df.write.format("delta").mode("overwrite").save(f"data/gold/{table_name}")
    print(f"{table_name}: {df.count()} rows written to Gold")

spark.stop()