# https://sparkbyexamples.com/pyspark/pyspark-mappartitions/
from pyspark.sql import SparkSession


def mapPartitionsExample(spark: SparkSession):
    data = [
        ("James", "Smith", "M", 3000),
        ("Anna", "Rose", "F", 4100),
        ("Robert", "Williams", "M", 6200),
    ]

    columns = ["firstname", "lastname", "gender", "salary"]
    df = spark.createDataFrame(data=data, schema=columns)

    # This function calls for each partition
    def reformat(partitionData):
        for row in partitionData:
            yield [row.firstname + "," + row.lastname, row.salary * 10 / 100]

    df2 = df.rdd.mapPartitions(reformat).toDF(["name", "bonus"])
    return df2
