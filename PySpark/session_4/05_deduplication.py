from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("JobPulse AI - Deduplication")
    .master("local[*]")
    .getOrCreate()
)

data = [
    (101, "Amazon", 90000),
    (102, "Google", 80000),
    (101, "Amazon", 90000),
    (103, "Amazon", 90000),
    (104, "Google", 85000),
]

columns = ["job_id", "company", "salary"]

df = spark.createDataFrame(data, columns)

df.show()

distinct_df = df.distinct()

distinct_df.show()

distinct_df.explain("formatted")

dedup_company_df = df.dropDuplicates(["company"])

dedup_company_df.show()

dedup_company_df.explain("formatted")
