from pyspark.sql import SparkSession
import sys
import traceback


def run_example_sc(function):
    try:
        spark = (
            SparkSession.builder.remote("sc://localhost")
            .appName("Example")
            .getOrCreate()
        )
        result = function(spark)
    except Exception:
        exc_type, _, _ = sys.exc_info()
        return False, f"{exc_type.__name__}: {traceback.format_exc()}"

    return True, result
