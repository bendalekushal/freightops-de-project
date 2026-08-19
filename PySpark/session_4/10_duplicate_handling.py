from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("DuplicateHandling") \
    .master("local[*]") \
    .getOrCreate()

dup_df = spark.createDataFrame([
    ("Kushal", "IT", 90000),
    ("Rahul", "HR", 60000),
    ("Amit", "IT", 70000),
    ("Sneha", "Finance", 80000),
    ("Priya", "HR", 75000),
    ("Rohan", "IT", 100000),
    ("Kushal", "IT", 90000),
    ("Rahul", "HR", 60000)
], ["name", "department", "salary"])

duplicates = (
    dup_df
    .groupBy("name", "department", "salary")
    .count()
    .filter(F.col("count") > 1)
)

duplicates.show()
duplicates.explain("formatted")

spark.stop()