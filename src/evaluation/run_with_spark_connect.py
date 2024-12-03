from pyspark.sql import SparkSession
import sys


def run_example_sc(function):
    try:
        spark = (
            SparkSession.builder.remote("sc://localhost")
            .appName("Example")
            .getOrCreate()
        )
        result = function(spark)
    except Exception as e:
        exc_type, _, _ = sys.exc_info()
        return False, f"{exc_type.__name__}: {e}"

    return True, result
