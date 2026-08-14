from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("JobPulse AI - Date Functions")
    .master("local[*]")
    .getOrCreate()
)

data = [
    (101, "Alice", "2026-08-01", "2026-08-05"),
    (102, "Bob", "2026-08-03", "2026-08-10"),
    (103, "Charlie", "2026-08-05", "2026-08-07"),
    (104, "David", "2026-08-10", "2026-08-15"),
]

columns = [
    "job_id",
    "candidate",
    "application_date",
    "joining_date"
]

df = spark.createDataFrame(data, columns)

df_typed = (df.withColumn(
    "application_date",
    F.to_date(F.col("application_date"), "yyyy-MM-dd")
    ).withColumn(
        "joining_date",
        F.to_date(F.col("joining_date"), "yyyy-MM-dd")
    ).withColumn(
        "days_to_join",
        F.datediff(F.col("joining_date"), F.col("application_date"))
    ).withColumn(
        "application_year",
        F.year(F.col("application_date"))
    ).withColumn(
        "application_month",
        F.month(F.col("application_date"))
    )
)

df_typed.printSchema()
df_typed.show()
df_typed.explain("formatted")