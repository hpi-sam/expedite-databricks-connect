from pyspark.sql import SparkSession


def mixedRDDExample(spark: SparkSession):
    # Example Text
    data = [
        "Spark is amazing",
        "RDD processing with Spark is powerful",
        "FlatMap and ReduceByKey are useful in Spark",
        "Spark is fast and scalable",
    ]

    # Create RDD
    rdd = spark.sparkContext.parallelize(data)

    # FlatMap: Split lines into words.
    words = rdd.flatMap(lambda line: line.split(" "))

    # Map: Create (word, 1) pairs
    word_pairs = words.map(lambda word: (word.lower(), 1))

    # ReduceByKey: Compute word count
    word_counts = word_pairs.reduceByKey(lambda a, b: a + b)

    # Filter: Only keep words that appear more than once
    frequent_words = word_counts.filter(lambda pair: pair[1] > 1)

    # Sort: Sort the words by count in descending order
    sorted_frequent_words = frequent_words.sortBy(lambda pair: pair[1], ascending=False)

    result = sorted_frequent_words.collect()
    return result
