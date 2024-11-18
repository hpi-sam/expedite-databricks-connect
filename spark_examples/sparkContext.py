from pyspark.sql import SparkSession

def sparkContextExample(spark: SparkSession):
    common_keys = [
        "spark.app.name",
        "spark.master",
    ]

    result = {}
    # Print configuration values
    for key in common_keys:
        value = spark.sparkContext.getConf().get(key)
        result[key] = value

    return result
