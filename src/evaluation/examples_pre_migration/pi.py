from random import random
from operator import add


def test_python_pi_issue(spark):
    """
    Test function for Pi computation focusing on identified issues at specific lines.
    """
    results = []

    partitions = 2  # Set a default partition number for the test
    n = 100000 * partitions

    def f(_):
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x**2 + y**2 <= 1 else 0

    # Line 41 issue - Problematic map-reduce operation
    count = (
        spark.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    )
    pi_value = round(4.0 * count / n)

    return [pi_value]
