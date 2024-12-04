from pyspark.sql import SparkSession, SQLContext


def test_sql_dataframe_reader_api(spark):
    """
    Function to test the dataframe reader API in PySpark. This function reproduces errors found in the provided Python file.
    :param spark: SparkSession object passed to the function
    :return: A list containing the result of the dataframe schema and types.
    """
    results = []
    # Error in line 18: Loading CSV file into a DataFrame.
    rdd = spark.sparkContext.textFile(
        "/raid/shared/masterproject2024/spark-examples/ages.csv"
    )
    df_csv = spark.read.option("header", "true").csv(rdd)
    results.append(df_csv.dtypes)

    # Error in line 33: Loading JSON file into a DataFrame using RDD.
    rdd_json = spark.sparkContext.textFile(
        "/raid/shared/masterproject2024/spark-examples/people.json"
    )
    df_json = spark.read.json(rdd_json)
    results.append(df_json.dtypes)

    return results
