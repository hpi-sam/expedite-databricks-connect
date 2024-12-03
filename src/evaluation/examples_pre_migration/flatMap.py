# https://sparkbyexamples.com/pyspark/pyspark-flatmap-transformation/
from pyspark.sql import SparkSession


def flatMapExample(spark):
    data = [
        "Project Gutenberg’s",
        "Alice’s Adventures in Wonderland",
        "Project Gutenberg’s",
        "Adventures in Wonderland",
        "Project Gutenberg’s",
    ]
    rdd = spark.sparkContext.parallelize(data)

    # Flatmap
    rdd2 = rdd.flatMap(lambda x: x.split(" "))
    result = []
    for element in rdd2.collect():
        result.append(element)

    return result
