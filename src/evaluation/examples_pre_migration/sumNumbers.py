from pyspark.sql import SparkSession
from pyspark import SparkContext


def sumNumbers(spark):
    """
    Function to test the pip sanity check by triggering the error on line 24 of the original script.
    """
    # Initialize the SparkContext from the provided SparkSession
    sc = spark.sparkContext

    # Create an RDD with parallelized data
    rdd = sc.parallelize(range(100), 10)

    # Reduce the RDD to compute the sum of all elements
    value = rdd.reduce(lambda x, y: x + y)

    # Trigger the issue at line 24
    return [value]
