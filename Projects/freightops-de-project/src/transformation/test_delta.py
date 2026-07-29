from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = SparkSession.builder \
    .appName("DeltaTest") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

data = [("test1", 1), ("test2", 2)]
df = spark.createDataFrame(data, ["name", "value"])

df.write.format("delta").mode("overwrite").save("data/delta_test")

result = spark.read.format("delta").load("data/delta_test")
result.show()

print("Delta Lake read/write test: SUCCESS")