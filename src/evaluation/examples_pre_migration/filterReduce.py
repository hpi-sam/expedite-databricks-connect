from pyspark.sql import SparkSession

def filterReduceExample(spark: SparkSession):
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    rdd = spark.sparkContext.parallelize(data)

    # Filter: Keep only even numbers
    even_numbers = rdd.filter(lambda x: x % 2 == 0)

    # Map: Square each even number
    squared_evens = even_numbers.map(lambda x: x ** 2)

    # Reduce: Calculate the sum of the squared even numbers
    sum_of_squared_evens = squared_evens.reduce(lambda x, y: x + y)

    return sum_of_squared_evens