from mapPartitions import mapPartitionsExample
from flatMap import flatMapExample
from mapReduce import mapReduceExample
from readJson import readJsonExample
from sparkContext import sparkContextExample
from map import mapExample
from sparkJvmOrigin import setJVMOrigin
from quinnRddSparkContext import quinn_rdd_spark_Context
from frequentWords import frequentWordsExample
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
