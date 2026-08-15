from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("orderByGlobalSorting") \
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

df = df.repartition(2)

print("Partitions:", df.rdd.getNumPartitions())

df.show()

# sorted_df = df.orderBy(
#     F.col("salary").desc()
# )

# sorted_df.show()

# print(spark.conf.get("spark.sql.shuffle.partitions"))

# sorted_df.explain("formatted")

locally_sorted_df = df.sortWithinPartitions(
    F.col("salary").desc()
)

locally_sorted_df.show()

locally_sorted_df.explain("formatted")

spark.stop()