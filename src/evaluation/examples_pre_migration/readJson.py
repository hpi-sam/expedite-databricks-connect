# Source: Migration Cheat Sheet
from pyspark.sql import SparkSession


def readJsonExample(spark: SparkSession):
    json_content1 = "{'json_col1': 'hello', 'json_col2': 32}"
    json_content2 = "{'json_col1': 'hello', 'json_col2': 'world'}"

    json_list = []
    json_list.append(json_content1)
    json_list.append(json_content2)

    df = spark.read.json(spark.sparkContext.parallelize(json_list))
    return df
