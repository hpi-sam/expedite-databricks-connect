# "https://github.com/mrpowers-io/quinn/pull/188/files from __future__ import annotations

from pyspark.sql import SparkSession, DataFrame
from typing import List
import sys
from pyspark.sql.types import StructField, StructType, IntegerType, StringType
import csv

def quinn_rdd_spark_Context(spark):
    def column_to_list(df: DataFrame, col_name: str):
        """Collect column to list of values.
        
        :param df: Input DataFrame
        :type df: pyspark.sql.DataFrame
        :param col_name: Column to collect
        :type col_name: str
        :return: List of values
        :rtype: List[Any]
        """
        
        pyarrow_valid = False
        pandas_valid = False

        if "pyarrow" in sys.modules and "pandas" in sys.modules:
            pyarrow_version = tuple(map(int, sys.modules["pyarrow"].__version__.split(".")))
            pandas_version = tuple(map(int, sys.modules["pandas"].__version__.split(".")))
            pyarrow_valid = pyarrow_version >= (0, 17, 0)
            pandas_valid = pandas_version >= (0, 24, 2)
        
        if pyarrow_valid and pandas_valid:
            return df.select(col_name).toPandas()[col_name].tolist()

        return [row[col_name] for row in df.select(col_name).collect()]

    spark = SparkSession.builder \
        .remote("sc://localhost") \
        .appName("Spark Connect Example") \
        .getOrCreate()

    data = [
        {"user_id": 1, "activity": "login"},
        {"user_id": 2, "activity": "view_product"},
        {"user_id": 1, "activity": "purchase"},
        {"user_id": 3, "activity": "logout"},
    ]
    schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("activity", StringType(), True),
    ])

    user_activity_df = spark.createDataFrame(data, schema=schema)

    user_ids: List[int] = column_to_list(user_activity_df, "user_id")

    return user_ids
