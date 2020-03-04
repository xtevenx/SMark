"""
The `stats` module contains the functions required to get statistical
attribute from a set of data.

  This module currently contains the following functions:
* mean  (arithmetic mean)
* stddev  (standard deviation)

All the functions in this module follow the simple format of accepting
a sequence of `float`s, the data of which to get the statistical
attribute for, and returning a float, the measure of the attribute.
Some functions may require/offer extra arguments to define
characteristic of the measured attribute.
"""

import math
from typing import Sequence


def mean(data: Sequence[float]) -> float:
    """
    Get the arithmetic mean of a sequence of numbers.
    """

    assert len(data) > 0

    return sum(data) / len(data)


def stddev(data: Sequence[float]) -> float:
    """
    Get the standard deviation of a sequence of numbers.
    """

    assert len(data) > 0

    mu = mean(data)
    return math.sqrt(sum((n - mu) ** 2 for n in data) / len(data))
