import math
from typing import Sequence


def mean(data: Sequence[float]) -> float:
    assert len(data) > 0

    return sum(data) / len(data)


def stddev(data: Sequence[float]) -> float:
    assert len(data) > 0

    mu = mean(data)
    return math.sqrt(sum((n - mu) ** 2 for n in data) / len(data))
