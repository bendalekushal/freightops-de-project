from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("DuplicateHandling") \
    .master("local[*]") \
    .getOrCreate()

df1 = spark.createDataFrame([
    ("Kushal", "IT", 90000),
    ("Rahul", "HR", 60000)
], ["name", "department", "salary"])

df2 = spark.createDataFrame([
    ("Amit", "IT", 70000),
    ("Sneha", "Finance", 80000)
], ["name", "department", "salary"])

df3 = df2.select(
    "name",
    "salary",
    "department"
)

df4 = spark.createDataFrame([
    ("Amit", "IT"),
    ("Sneha", "Finance")
], ["name", "department"])

# df1.unionByName(df4).show()

result = df1.unionByName(df4, allowMissingColumns=True)

result.show()
result.explain("formatted")

spark.stop()