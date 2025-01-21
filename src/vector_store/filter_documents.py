import json


def filter_documents():
    path = "/raid/shared/masterproject2024/rag/data/api_reference_new.json"
    destination_path = (
        "/raid/shared/masterproject2024/rag/data/api_reference_filtered.json"
    )
    filtered_urls = [
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/core_classes.html",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.pandas/",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.html",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.errors.html",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/configuration.html",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/io.html",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/data_types.html",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/row.html",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/grouping.html",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/avro.html",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/observation.html",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/protobuf.html",
    ]

    with open(path) as handle:
        docs = json.loads(handle.read())
    print(len(docs))

    # Filter out documents where source is link
    docs = [
        doc
        for doc in docs
        if not (
            doc["metadata"]["source"].startswith(filtered_urls[0])
            or doc["metadata"]["source"] in filtered_urls
        )
    ]

    print(len(docs))

    # Save to json file
    with open(destination_path, "w") as handle:
        handle.write(json.dumps(docs))


filter_documents()
