from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("JobPulse AI - String Functions")
    .master("local[*]")
    .getOrCreate()
)

data = [
    (101, "  Microsoft  ", "PUNE, India"),
    (102, "AMAZON", "Mumbai, INDIA"),
    (103, "google india", "Bangalore, India"),
    (104, "  TCS", "PUNE, INDIA"),
]

columns = ["job_id", "company", "location"]

df = spark.createDataFrame(data, columns)

df.show(truncate=False)

clean_df = df.withColumn(
    "company_clean",
    F.trim(F.lower(F.col("company"))),
).withColumn(
    "city_clean",
    F.trim(F.lower(F.split(F.col("location"), ",")[0]))
)
clean_df.show(truncate=False)

clean_df.explain("formatted")

spark.stop()