from pyspark.sql import SparkSession


def frequentWordsExample(spark: SparkSession):

    # Sample data as a list of lines
    data = [
        "Apache Spark is an open-source unified analytics engine.",
        "It is used for big data processes, with built-in modules.",
        "Modules include SQL, machine learning, and graph processing.",
        "ApacheSpark is fast and supports multiple languages like Python and Java, and Scala.",
    ]

    # Create an RDD from the sample data
    lines = spark.sparkContext.parallelize(data)

    # Transform the lines into words (flatMap splits each line into words)
    words = lines.flatMap(lambda line: line.split(" "))

    # Map each word to a tuple (word, 1)
    word_tuples = words.map(lambda word: (word.lower().strip(".,!?"), 1))

    # Reduce by key to count occurrences of each word
    word_counts = word_tuples.reduceByKey(lambda a, b: a + b)

    # Sort the word counts in descending order
    sorted_word_counts = word_counts.sortBy(lambda pair: pair[1], ascending=False)

    # Take the top N words (e.g., top 3)
    top_n_words = sorted_word_counts.take(3)

    return top_n_words
