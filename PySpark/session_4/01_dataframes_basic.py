from pandas import col
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("JobPulse AI - Session 4")
    .master("local[*]")
    .getOrCreate()
)

data = [
    (101, "Alice", "IT", 75000),
    (102, "Bob", "HR", 55000),
    (103, "Charlie", "IT", 90000),
    (104, "David", "Finance", 65000),
]

columns = ["employee_id", "name", "department", "salary"]

df = spark.createDataFrame(data, columns)

employees_df = spark.read.parquet("PySpark/session_4/data/employees")

filtered_employees = employees_df\
    .filter((F.col("salary") > 60000) & (F.col("department") == "IT"))\
    .select("name", "salary", "department")

# result = (
#     employees_df
#     .filter(
#         (F.col("salary") > 60000) |
#         (F.col("department") == "IT")
#     )
#     .select("name", "department", "salary")
# )

# result.show()

# result.explain("formatted")

# salary_band_df = employees_df.withColumn(
#     "salary_band",
#     F.when(F.col("salary") < 60000, "Low")
#     .when((F.col("salary") >= 60000) & (F.col("salary") < 80000), "Medium")
#     .otherwise("High")
# )

# salary_band_df.show()

# salary_band_df.explain("formatted")

employees_messy = employees_df.withColumn(
    "salary_string",
    F.col("salary").cast("string")
)

employees_messy.printSchema()

employees_typed = employees_messy.withColumn(
    "salary_numeric",
    F.col("salary_string").cast("double")
)

employees_typed.printSchema()
employees_typed.show()

employees_final = employees_typed.withColumn(
    "country",
    F.lit("India")
)

employees_final.show()

spark.stop()

