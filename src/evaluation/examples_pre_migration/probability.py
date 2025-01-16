from random import random, seed
from operator import add


def probabilityExample(spark):
    """
    Estimate the probability that two random points on a line are within a given distance, 
    with deterministic output by seeding the random number generator.
    """
    partitions = 2  # Set a default number of partitions
    n = 100000 * partitions  # Total number of simulations

    threshold = 0.5  # Maximum distance for the points to be "close"

    # Seed the random number generator
    seed(42)

    def within_threshold(_):
        point1 = random()
        point2 = random()
        return 1 if abs(point1 - point2) <= threshold else 0

    count = (
        spark.sparkContext.parallelize(range(1, n + 1), partitions)
        .map(within_threshold)
        .reduce(add)
    )
    probability = round(count / n, 2)  # Estimate the probability to 2 decimal places

    return [probability]