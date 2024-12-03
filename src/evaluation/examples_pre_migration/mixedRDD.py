from pyspark.sql import SparkSession


def mixedRDDExample(spark: SparkSession):
    # Beispieltext
    data = [
        "Spark is amazing",
        "RDD processing with Spark is powerful",
        "FlatMap and ReduceByKey are useful in Spark",
        "Spark is fast and scalable",
    ]

    # RDD erstellen
    rdd = spark.sparkContext.parallelize(data)

    # FlatMap: Zeilen in Wörter aufteilen
    words = rdd.flatMap(lambda line: line.split(" "))

    # Map: Wörter in (Wort, 1) Paare umwandeln
    word_pairs = words.map(lambda word: (word.lower(), 1))

    # ReduceByKey: Wortanzahl berechnen
    word_counts = word_pairs.reduceByKey(lambda a, b: a + b)

    # Filter: Nur Wörter mit mehr als einem Vorkommen behalten
    frequent_words = word_counts.filter(lambda pair: pair[1] > 1)

    result = frequent_words.collect()
    return result
