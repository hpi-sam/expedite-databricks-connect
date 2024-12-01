from pyspark.sql import SparkSession

def filterExample(spark: SparkSession):
    data = [
        (1, "Alice", 25),
        (2, "Bob", 30),
        (3, "Charlie", 35),
        (4, "David", 40),
        (5, "Eve", 45)
    ]

    rdd = sparkContext.parallelize(data)

    # Filter rows where age > 25
    filtered_rdd = rdd.filter(lambda x: x[2] > 25)
    
    res = []
    for element in filtered_rdd.collect():
        res.append(element)

    return res

