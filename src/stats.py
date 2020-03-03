import math
from typing import Sequence


def mean(data: Sequence[float]) -> float:
    """
    Get the arithmetic mean of a sequence of numbers.
    :param data: the `Sequence` of which to get the mean of.
    :return: a `float`, the mean of the sequence `data`.
    """

    assert len(data) > 0

    return sum(data) / len(data)


def stddev(data: Sequence[float]) -> float:
    """
    Get the standard deviation of a sequence of numbers.
    :param data: the `Sequence` of which to get the standard deviation
        of.
    :return: a `float`, the standard deviation of the sequence `data`.
    """

    assert len(data) > 0

    mu = mean(data)
    return math.sqrt(sum((n - mu) ** 2 for n in data) / len(data))
