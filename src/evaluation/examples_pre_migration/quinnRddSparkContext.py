# "https://github.com/mrpowers-io/quinn/pull/188/files from __future__ import annotations

from typing import TYPE_CHECKING
from pyspark.sql import DataFrame
import sys
from typing import Any
from pyspark.sql.types import StructField, StructType, IntegerType, StringType
from typing import List
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
        pyarrow_kv = ("spark.sql.execution.arrow.pyspark.enabled", "true")
        if "pyspark" not in sys.modules:
            raise ImportError

        # sparksession from df is not available in older versions of pyspark
        if sys.modules["pyspark"].__version__ < "3.3.0":
            return df.select(col_name).rdd.flatMap(lambda x: x).collect()

        spark_config = df.sparkSession.sparkContext.getConf().getAll()

        pyarrow_enabled: bool = pyarrow_kv in spark_config
        pyarrow_valid = pyarrow_enabled and sys.modules["pyarrow"] >= "0.17.0"
        pandas_exists = "pandas" in sys.modules
        pandas_valid = pandas_exists and sys.modules["pandas"].__version__ >= "0.24.2"
        if pyarrow_valid and pandas_valid:
            return df.select(col_name).toPandas()[col_name].tolist()

        return df.select(col_name).rdd.flatMap(lambda x: x).collect()

    data = [
        {"user_id": 1, "activity": "login"},
        {"user_id": 2, "activity": "view_product"},
        {"user_id": 1, "activity": "purchase"},
        {"user_id": 3, "activity": "logout"},
    ]
    schema = StructType(
        [
            StructField("user_id", IntegerType(), True),
            StructField("activity", StringType(), True),
        ]
    )

    user_activity_df = spark.createDataFrame(data, schema=schema)

    user_ids: List[int] = column_to_list(user_activity_df, "user_id")

    return user_ids
