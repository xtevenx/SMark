import enum
import math
import statistics
from typing import Callable, List, Sequence

_SCALE_FUNCTION = Callable[[Sequence[float], float], List[float]]


class Direction(enum.Enum):
    UP: str = "up"
    DOWN: str = "down"


def scale(data: Sequence[float], target: float) -> List[float]:
    """Scale a sequence of numbers to a specific arithmetic mean.

    Output a sequence of numbers (in the range 0 to 1) which have the following
    properties:

    -   The output sequence is in the same order as the input sequence.
    -   The values in the sorted input sequence are in the same order as the
        values in the sorted output sequence. In other words, for all values
        ``x`` and ``y`` in the input sequence, if ``x`` is less than ``y``,
        then the scaled value of ``x`` is less than the scaled value of ``y``.
    -   The arithmetic mean of the values is ``target``.

    :param data: The sequence of floats to scale. All the numbers in this
        sequence must be between 0 and 1.
    :param target: A float representing the arithmetic mean of the output
        sequence. This number must be between 0 and 1.
    :return: A sequence of floats abiding by the properties described above.
    """

    assert all(0 <= n <= 1 for n in data) and 0 <= target <= 1

    scale_func = inverse_power_scale if target > statistics.mean(data) else power_scale

    def scale_result(n: float) -> float:
        return statistics.mean(scale_func(data, n))

    scale_factor = _geometric_binary_search(scale_result, target)
    return scale_func(data, scale_factor)


def inverse_power_scale(data: Sequence[float], power: float) -> List[float]:
    """Scale a sequence of numbers based on the ``inverse_power_scale``.

    The ``inverse_power_scale`` scales the distribution of numbers inversely
    proportional to the ``power_scale``. While the ``power_scale`` places more
    emphasis in scaling the lower values, the ``inverse_power_scale`` places
    more emphasis in scaling the higher values. This is beneficial when one
    wishes to keep the distribution of numbers wide when scaling up.

    :param data: The sequence of floats to scale. The floats must be between
        zero and one, and will also be scaled within that range.
    :param power: A positive float representing the scaling factor. A larger
        number results in scaling the numbers higher. A scaling factor of 1 has
        no effect.
    :return: The sequence of floats after scaling. The floats in the sequence
        remain in the order they were given and the ``data`` is not modified.
    """

    return [1 - (1 - n) ** power for n in data]


def power_scale(data: Sequence[float], power: float) -> List[float]:
    """Scale a sequence of numbers based on the ``power_scale``.

    The ``power_scale`` is a variable tweak of the commonly used scaling method
    where one scales a score, :math:`x,\\ 0 \\leq x \\leq 100`, by multiplying
    the square root of :math:`x` by a factor of 10, namely:

    .. math:: s(x) = 10 \\left( x ^ {\\frac{1}{2}} \\right)

    The ``power_scale`` allows the variation of the exponent (in the example,
    :math:`\\frac{1}{2}`) to achieve variable scaling rates.

    :param data: The sequence of floats to scale. The floats must be between
        zero and one, and will also be scaled within that range.
    :param power: A positive float representing the scaling factor. A larger
        number results in scaling the numbers higher. A scaling factor of 1 has
        no effect.
    :return: The sequence of floats after scaling. The floats in the sequence
        remain in the order they were given and the ``data`` is not modified.
    """

    return [n ** (1 / power) for n in data]


def _rational_scale(x: float, factor: float, direc: Direction = Direction.UP) -> float:
    """Helper function for ``rational_scale()``."""
    disc = math.sqrt(factor * (factor + 4))
    p = (-factor + (1 if direc == Direction.UP else -1) * disc) / 2
    return (factor * x) / (p * (factor * x + p))


def rational_scale(
        data: Sequence[float],
        factor: float,
        direc: Direction = Direction.UP
) -> List[float]:
    """Scale a sequence of numbers based on the ``rational_scale``.

    The ``rational_scale`` is basically a transformation of the simple rational
    function in the form :math:`f(x) = \\frac{1}{x}` such that :math:`f(0) = 0`
    and :math:`f(1) = 1`. Some math derives the formula of the rational curve
    that fits the above conditions as:

    .. math:: s(x) = \\frac{ax}{p(ax + p)}

    where :math:`a` is the scaling factor, and:

    .. math:: p = \\frac{-a + \\sqrt{a(a + 4)}}{2}

    for the curve scaling up and:

    .. math:: p = \\frac{-a - \\sqrt{a(a + 4)}}{2}

    for the curve scaling down.

    This curve is symmetrical on :math:`y = -x + b` which may or may not have a
    practical benefit, but the definite benefit is that it looks nice. :D

    :param data: The sequence of floats to scale. The floats must be between
        zero and one, and will also be scaled within that range.
    :param factor: A positive float representing the scaling factor. A larger
        number results in more scaling. A scaling factor of 0 has no effect.
    :param direc: A Direction type signifying which direction to scale the
        marks.
    :return: The sequence of floats after scaling. The floats in the sequence
        remain in the order they were given and the ``data`` is not modified.
    """

    return [_rational_scale(x, factor, direc) for x in data]


def _geometric_binary_search(
        func: Callable[[float], float],
        target: float,
        iterations: int = 24,
        reverse: bool = False
) -> float:
    """Perform a binary search using geometric centers.

    Do a binary search to find the value ``n`` that makes the function ``func``
    return ``target`` when ``n`` is used as the argument. By default, it is
    assumed that smaller values of ``n`` will cause ``func`` to produce smaller
    outputs. If smaller values of ``n`` produce larger outputs, set ``reverse``
    to True.

    This implementation of binary search uses the geometric mean instead of the
    arithmetic mean to determine the center of the search space. This is
    because the values that are being searched are weighted towards zero.

    :param func: A Callable which accepts a float and returns a float. This
        must be a one-to-one function.
    :param target: A float representing the target output which we are trying
        to make func produce.
    :param iterations: An integer representing the number of iterations to run
        the binary search. The default of 24 should be sufficient for most
        applications.
    :param reverse: A bool representing the relationship between the input and
        output values of func.
    :return: A float representing value n which makes the function func produce
        target when called as its argument.
    """

    lower_bound = 2 ** -iterations
    upper_bound = 2 ** iterations
    assert lower_bound <= upper_bound

    for _ in range(iterations):
        guess = math.sqrt(lower_bound * upper_bound)
        answer = func(guess)

        if (not reverse and answer > target) or (reverse and answer < target):
            upper_bound = guess
        else:
            lower_bound = guess

    return math.sqrt(lower_bound * upper_bound)
