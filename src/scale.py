import math
from typing import Callable, List, Sequence

import statistics

_SCALE_FUNCTION = Callable[[Sequence[float], float], List[float]]


def scale(data: Sequence[float], target: float, scale_func: _SCALE_FUNCTION
          ) -> (List[float], float):
    assert all(0 <= n <= 1 for n in data)
    assert 0 <= target <= 1

    def scale_result(n: float) -> float:
        return statistics.mean(scale_func(data, n))

    scale_factor = _binary_search(
        lower_bound=0, upper_bound=2 ** 64, target=target, func=scale_result
    )

    return scale_func(data, scale_factor), scale_factor


def inverse_power_scale(data: Sequence[float], power: float) -> List[float]:
    """Scale a sequence of numbers based on the ``inverse_power_scale``.

    The ``inverse_power_scale`` scales the distribution of numbers inversely
    proportional to the ``power_scale``. While the ``power_scale`` places more
    emphasis in scaling the lower values, the ``inverse_power_scale`` places
    more emphasis in scaling the higher values. This is beneficial when one
    wishes to keep the distribution of numbers wide when scaling up.

    :param data: The sequence of floats to scale.
    :param power: A float representing the scaling factor. A number greater
        than one results in the numbers of the sequence being scaled upwards
        where a larger number represents more scaling. A number less than one
        results in the numbers being scaled downwards where a smaller number
        represents more scaling.
    :return: The sequence of floats after scaling. The floats in the sequence
        remain in the order they were given and the ``data`` is not modified.
    """

    return [1 - (1 - n) ** power for n in data]


def power_scale(data: Sequence[float], power: float) -> List[float]:
    """Scale a sequence of numbers based on the ``power_scale``.

    The ``power_scale`` is a variable tweak of the commonly used scaling method
    where one scales a score, ``n`` {0 <= n <= 100}, by multiplying the square
    root of ``n`` by a factor of 10, namely:

    .. math::

        n_{scaled} = 10 \\left( n_{original} ^ {\\frac{1}{2}} \\right)

    The ``power_scale`` allows the variation of the exponent (in the example,
    :math:`\\frac{1}{2}`) to achieve variable scaling rates.

    :param data: The sequence of floats to scale.
    :param power: A float representing the scaling factor. A number less than
        one results in the numbers of the sequence being scaled upwards where a
        smaller number represents more scaling. A number greater than one
        results in the numbers being scaled downwards where a larger number
        represents more scaling.
    :return: The sequence of floats after scaling. The floats in the sequence
        remain in the order they were given and the ``data`` is not modified.
    """

    return [n ** (1 / power) for n in data]


def _binary_search(lower_bound: float, upper_bound: float, target: float,
                   func: Callable[[float], float],
                   precision: float = 2 ** -52,
                   reverse: bool = False) -> float:
    assert upper_bound > lower_bound

    search_iterations = math.log2((upper_bound - lower_bound) / precision)
    for _ in range(int(search_iterations + 1)):
        guess = (lower_bound + upper_bound) / 2
        answer = func(guess)

        if (not reverse and answer > target) or (reverse and answer < target):
            upper_bound = guess
        else:
            lower_bound = guess

    return (lower_bound + upper_bound) / 2
