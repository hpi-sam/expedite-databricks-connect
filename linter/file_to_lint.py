# test_file.py

df = spark.read.csv("file.csv")
rdd = df.rdd
rdd = df.rdd
result = rdd.mapPartitions(lambda x: x)