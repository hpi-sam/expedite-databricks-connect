from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql import Row
from pyspark.ml.fpm import PrefixSpan


def test_prefix_span_example(spark):
    """
    This function tests the PrefixSpan functionality and demonstrates the error in line 36.
    It uses different numbers in the sequences.
    """
    # Create an RDD and convert it to a DataFrame
    sc = spark.sparkContext
    df = sc.parallelize(
        [
            Row(sequence=[[10, 20], [30]]),
            Row(sequence=[[10], [30, 20], [10, 20]]),
            Row(sequence=[[10, 20], [50]]),
            Row(sequence=[[60]]),
        ]
    ).toDF()

    # Configure PrefixSpan with parameters
    prefixSpan = PrefixSpan(
        minSupport=0.5, maxPatternLength=5, maxLocalProjDBSize=32000000
    )

    # Trigger the operation and return the results as a list
    results = prefixSpan.findFrequentSequentialPatterns(
        df
    ).collect()  # Avoiding .show()
    return [row.asDict() for row in results]
