from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from delta import configure_spark_with_delta_pip
from delta.tables import DeltaTable

builder = SparkSession.builder\
    .appName("SCDUpdateDrivers")\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

drivers_df = spark.read.format("delta").load("data/silver/drivers")

updated_drivers_df = drivers_df.withColumn(
    "home_terminal",
    F.when(F.col("driver_id") == "DRV00001", F.lit("Chicago")).otherwise(F.col("home_terminal"))
)

dim_driver_table = DeltaTable.forPath(spark, "data/gold/dim_driver")

dim_driver_table.alias("target").merge(
    updated_drivers_df.alias("source"),
    "target.driver_id = source.driver_id AND target.is_current = true"
).whenMatchedUpdate(
    condition="target.home_terminal != source.home_terminal",
    set={
        "is_current": F.lit(False),
        "effective_end_date": F.current_date()
    }
).execute()

dim_driver_table.alias("target").merge(
    updated_drivers_df.alias("source"),
    "target.driver_id = source.driver_id AND target.is_current = true"
).whenNotMatchedInsert(
    values={
        "driver_id": "source.driver_id",
        "first_name": "source.first_name",
        "last_name": "source.last_name",
        "hire_date": "source.hire_date",
        "termination_date": "source.termination_date",
        "license_number": "source.license_number",
        "license_state": "source.license_state",
        "date_of_birth": "source.date_of_birth",
        "home_terminal": "source.home_terminal",
        "employment_status": "source.employment_status",
        "cdl_class": "source.cdl_class",
        "years_experience": "source.years_experience",
        "effective_start_date": "current_date()",
        "effective_end_date": "cast(null as date)",
        "is_current": "true"
    }
).execute()

spark.read.format("delta")\
    .load("data/gold/dim_driver")\
    .filter(F.col("driver_id") == "DRV00001")\
    .show()

spark.stop()