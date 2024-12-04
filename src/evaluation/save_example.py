from examples_pre_migration.mapPartitions import mapPartitionsExample
from examples_pre_migration.flatMap import flatMapExample
from examples_pre_migration.mapReduce import mapReduceExample
from examples_pre_migration.readJson import readJsonExample
from examples_pre_migration.sparkContext import sparkContextExample
from examples_pre_migration.map import mapExample
from examples_pre_migration.quinnRddSparkContext import quinn_rdd_spark_Context
from examples_pre_migration.frequentWords import frequentWordsExample
from examples_pre_migration.pi import test_python_pi_issue
from examples_pre_migration.prefixSpan import test_prefix_span_example
from examples_pre_migration.readJsonCsv import test_sql_dataframe_reader_api
from examples_pre_migration.sumNumbers import sumNumbers
from pyspark.sql import SparkSession
import pandas as pd

spark = SparkSession.builder.appName("Example").getOrCreate()

mapPartitionsExample(spark).toPandas().to_csv("output/mapPartitions.csv")
pd.DataFrame(flatMapExample(spark)).to_csv(
    "output/flatMap.csv", index=False, header=False
)
pd.DataFrame([mapReduceExample(spark)]).to_csv(
    "output/mapReduce.csv", index=False, header=False
)
readJsonExample(spark).toPandas().to_csv("output/readJson.csv")
pd.DataFrame(sparkContextExample(spark).items()).to_csv(
    "output/sparkContext.csv", index=False, header=False
)
pd.DataFrame(mapExample(spark)).to_csv("output/map.csv", index=False, header=False)

pd.DataFrame(quinn_rdd_spark_Context(spark)).to_csv(
    "output/quinnRddSparkContext.csv", index=False, header=False
)

pd.DataFrame(frequentWordsExample(spark)).to_csv(
    "output/frequentWords.csv", index=False, header=False
)

pd.DataFrame(sumNumbers(spark)).to_csv(
    "output/sumNumbers.csv", index=False, header=False
)

pd.DataFrame(test_sql_dataframe_reader_api(spark)).to_csv(
    "output/readJsonCsv.csv", index=False, header=False
)

pd.DataFrame(test_python_pi_issue(spark)).to_csv(
    "output/pi.csv", index=False, header=False
)

pd.DataFrame(test_prefix_span_example(spark)).to_csv(
    "output/prefixSpan.csv", index=False, header=False
)
