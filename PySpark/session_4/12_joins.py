from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("Joins") \
    .master("local[*]") \
    .getOrCreate()

employees = spark.createDataFrame([
    (1, "Kushal", "IT", 90000),
    (2, "Rahul", "HR", 60000),
    (3, "Amit", "IT", 70000),
    (4, "Sneha", "Finance", 80000)
], ["id", "name", "department", "salary"])

departments = spark.createDataFrame([
    ("IT", "Bangalore"),
    ("HR", "Mumbai"),
    ("Finance", "Pune")
], ["department", "location"])

salary_bands = spark.createDataFrame([
    ("Junior", 0, 70000),
    ("Mid", 70001, 90000),
    ("Senior", 90001, 200000)
], ["level", "min_salary", "max_salary"])

# sort merge join

# result = employees.join(
#     departments,
#     employees.department == departments.department,
#     "inner"
# )

# broadcast hash join

# result = F.broadcast(departments).join(
#         employees,
#         employees.department == departments.department,
#         "inner"
#     )

# broadcast nested loop join

# result = employees.join(
#     F.broadcast(salary_bands),
#     (employees.salary >= salary_bands.min_salary) &
#     (employees.salary <= salary_bands.max_salary),
#     "inner"
# )

# shuffle hash join

spark.conf.set(
    "spark.sql.join.preferSortMergeJoin",
    "false"
)

result = employees.join(
    departments,
    employees.department == departments.department,
    "inner"
)

result.show()
result.explain("formatted")

result.show()
result.explain("formatted")

spark.stop()