from pyspark.sql import SparkSession

def sumSquaresExample(spark):
    """
    Computes the sum of squares of odd numbers from 0 to 99.
    """
    # Initialize the SparkContext from the provided SparkSession
    sc = spark.sparkContext

    # Create an RDD with parallelized data
    rdd = sc.parallelize(range(100), 10)

    # Filter to retain only odd numbers
    odd_numbers = rdd.filter(lambda x: x % 2 != 0)

    # Map each odd number to its square
    squares = odd_numbers.map(lambda x: x ** 2)

    # Reduce to compute the sum of all squared values
    sum_squares = squares.reduce(lambda x, y: x + y)

    # make int
    sum_squares = int(sum_squares)

    # Return the computed sum
    return [sum_squares]
