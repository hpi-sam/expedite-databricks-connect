from pyspark.sql import SparkSession


def mapReduceExample(spark: SparkSession):
    data = [1, 2, 2, 1, 3, 2, 1, 3, 2, 4, 2, 2, 1, 4, 3, 2, 3, 1]

    rdd = spark.sparkContext.parallelize(data)

    rdd2 = rdd.map(lambda x: x * 2)
    sum = rdd2.reduce(lambda x, y: x + y)

    return sum
