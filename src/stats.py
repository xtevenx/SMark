"""
The `stats` module contains the functions required to get statistical
attribute from a set of data.

  This module currently contains the following functions:
* mean  (arithmetic mean)
* median  (median)
* stddev  (standard deviation)

All the functions in this module follow the simple format of accepting
a sequence of `float`s, the data of which to get the statistical
attribute for, and returning a float, the measure of the attribute.
Some functions may require/offer extra arguments to define
characteristic of the measured attribute.
"""

import math
from typing import Sequence


def _assert_valid_sequence(foo):
    def _decorated(data: Sequence[float], **kwargs) -> float:
        assert len(data) > 0 and all(type(x) == float for x in data)
        return foo(data, **kwargs)

    return _decorated


@_assert_valid_sequence
def mean(data: Sequence[float]) -> float:
    """
    Get the arithmetic mean of a sequence of numbers.
    """

    return sum(data) / len(data)


@_assert_valid_sequence
def median(data: Sequence[float]) -> float:
    """
    Get the median of a sequence of numbers.
    """

    midpoint_index, r = divmod(len(data), 2)
    if r:
        return data[midpoint_index]
    else:
        return (data[midpoint_index - 1] + data[midpoint_index]) / 2


@_assert_valid_sequence
def stddev(data: Sequence[float]) -> float:
    """
    Get the standard deviation of a sequence of numbers.
    """

    mu = mean(data)
    return math.sqrt(sum((n - mu) ** 2 for n in data) / len(data))
