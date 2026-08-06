from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from delta import configure_spark_with_delta_pip
from delta.tables import DeltaTable

builder = SparkSession.builder\
    .appName("SCDUpdateTrucks")\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

trucks_df = spark.read.format("delta").load("data/silver/trucks")

updated_trucks_df = trucks_df.withColumn(
    "status",
    F.when(F.col("truck_id") == "TRK00001", F.lit("Maintenance")).otherwise(F.col("status"))
)

dim_truck_table = DeltaTable.forPath(spark, "data/gold/dim_truck")

dim_truck_table.alias("target").merge(
    updated_trucks_df.alias("source"),
    "target.truck_id = source.truck_id AND target.is_current = true"
).whenMatchedUpdate(
    condition="target.status != source.status",
    set={
        "is_current": F.lit(False),
        "effective_end_date": F.current_date()
    }
).execute()

dim_truck_table.alias("target").merge(
    updated_trucks_df.alias("source"),
    "target.truck_id = source.truck_id AND target.is_current = true"
).whenNotMatchedInsert(
    values={
        "truck_id": "source.truck_id",
        "unit_number": "source.unit_number",
        "make": "source.make",
        "model_year": "source.model_year",
        "vin": "source.vin",
        "acquisition_date": "source.acquisition_date",
        "acquisition_mileage": "source.acquisition_mileage",
        "fuel_type": "source.fuel_type",
        "tank_capacity_gallons": "source.tank_capacity_gallons",
        "status": "source.status",
        "home_terminal": "source.home_terminal",
        "effective_start_date": "current_date()",
        "effective_end_date": "cast(null as date)",
        "is_current": "true"
    }
).execute()

spark.read.format("delta")\
    .load("data/gold/dim_truck")\
    .filter(F.col("truck_id") == "TRK00001")\
    .show()

spark.stop()