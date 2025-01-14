from pyspark.sql import SparkSession

def frequentLettersExample(spark: SparkSession):

    # Beispiel-Daten als Liste von Strings
    data = [
        "Apache Spark is a powerful engine for big data processing.",
        "It supports multiple languages like Python, Java, and Scala.",
        "With its high performance, Spark is widely adopted in the industry.",
    ]

    # Erstelle ein RDD aus den Beispiel-Daten
    lines = spark.sparkContext.parallelize(data)

    # Transformiere die Zeilen in einzelne Buchstaben (flatMap spaltet in Zeichen auf)
    letters = lines.flatMap(lambda line: [char.lower() for char in line if char.isalpha()])

    # Map: Jedes Zeichen wird einem Tupel (Buchstabe, 1) zugeordnet
    letter_tuples = letters.map(lambda letter: (letter, 1))

    # ReduceByKey: Zähle die Häufigkeit jedes Buchstabens
    letter_counts = letter_tuples.reduceByKey(lambda a, b: a + b)

    # Sortiere die Buchstaben nach Häufigkeit absteigend
    sorted_letter_counts = letter_counts.sortBy(lambda pair: pair[1], ascending=False)

    # Nimm die Top N Buchstaben (z. B. die 5 häufigsten)
    top_n_letters = sorted_letter_counts.take(5)

    return top_n_letters
