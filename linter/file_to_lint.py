# test_file.py

df = spark.read.csv("file.csv")
rdd = df.emptyRDD()
rdd = df.parallelize()
spark.sparkContext.setLogLevel("ERROR") 
result = rdd.mapPartitions(lambda x: x)
