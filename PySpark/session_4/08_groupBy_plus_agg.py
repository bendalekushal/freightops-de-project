from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("RepartitionExample") \
    .master("local[*]") \
    .getOrCreate()

data = [
    ("Kushal", "IT", 90000),
    ("Rahul", "HR", 60000),
    ("Amit", "IT", 70000),
    ("Sneha", "Finance", 80000),
    ("Priya", "HR", 75000),
    ("Rohan", "IT", 100000)
]

columns = ["name", "department", "salary"]

df = spark.createDataFrame(data, columns)

# result = df.groupBy("department").agg(
#     F.count("*").alias("employee_count"),
#     F.sum("salary").alias("total_salary"),
#     F.avg("salary").alias("avg_salary"),
#     F.min("salary").alias("min_salary"),
#     F.max("salary").alias("max_salary")
# )

# result = (
#     df.filter(F.col("salary") >= 75000)
#     .groupBy("department")
#     .agg(
#         F.count("*").alias("employee_count"),
#         F.sum("salary").alias("total_salary")
#     )
# )

result = (
    df
    .groupBy("department")
    .agg(
        F.sum("salary").alias("total_salary")
    )
    .filter(F.col("total_salary") > 150000)
)

result.show()
result.explain("formatted")

result.show()

result.explain("formatted")

spark.stop()