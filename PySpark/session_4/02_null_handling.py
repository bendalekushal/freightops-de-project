from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("JobPulse AI - NULL Handling")
    .master("local[*]")
    .getOrCreate()
)

data = [
    (101, "Alice", 75000),
    (102, "Bob", None),
    (103, "Charlie", 55000),
    (104, "David", None),
    (105, "Eva", 90000),
]

columns = ["employee_id", "name", "salary"]

df = spark.createDataFrame(data, columns)

df.printSchema()
filtered_df = df.fillna({"salary":0})
filtered_df.show()
# df.show()

dropped_df = df.dropna(subset=["salary"])

dropped_df.show()

coalesced_df = df.withColumn(
    "salary_clean",
    F.coalesce(F.col("salary"), F.lit(0))
)
coalesced_df.show()
# non_null_salary_df.show()

# result = df.withColumn(
#     "salary_status",
#     F.when(F.col("salary") > 60000, "Above 60K")
#      .otherwise("60K or Below")
# )

# result.show()

spark.stop()