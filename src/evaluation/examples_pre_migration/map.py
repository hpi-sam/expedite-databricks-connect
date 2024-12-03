# Source: Migration Cheat Sheet
from pyspark.sql import SparkSession


def mapExample(spark: SparkSession):
    df = spark.createDataFrame([("Alice", 100), ("Bob", 200)], ["name", "age"])
    result = df.rdd.map(lambda row: f"{row.name=} {row.age=}").collect()
    return result
