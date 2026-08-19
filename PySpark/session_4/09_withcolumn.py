from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("withColumnExample") \
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

# result = (
#     df
#     .withColumn("annual_salary", F.col("salary") * 12)
#     .withColumn("monthly_bonus", F.col("salary") * 0.10)
#     .withColumn(
#         "total_compensation",
#         F.col("annual_salary") + (F.col("monthly_bonus") * 12)
#     )
# )

# result = df.drop("name")
# result.show()

result = df.dropDuplicates(["department"])

result.show()



print("Original partitions:", df.rdd.getNumPartitions())
print("New partitions:", result.rdd.getNumPartitions())

result.explain("formatted")

spark.stop()
