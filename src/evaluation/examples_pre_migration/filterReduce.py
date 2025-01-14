from pyspark.sql import SparkSession

def filterReduceExample(spark: SparkSession):
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    rdd = spark.sparkContext.parallelize(data)

    # Map: Annotate each number with its parity (even or odd)
    annotated = rdd.map(lambda x: ("even" if x % 2 == 0 else "odd", x))

    # GroupByKey: Group numbers by their parity
    grouped = annotated.groupByKey()

    # ReduceByKey: Sum the numbers in each group
    summed = grouped.mapValues(lambda nums: sum(nums))

    # Convert the results into a dictionary
    result = summed.collectAsMap()

    return result