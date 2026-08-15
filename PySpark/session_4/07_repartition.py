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

print("Original partitions:", df.rdd.getNumPartitions())

df_repartitioned = df.repartition(2, "department")

print("after repartitioning:"
      , df_repartitioned.rdd.getNumPartitions()
)

df_repartitioned.explain("formatted")

spark.stop()